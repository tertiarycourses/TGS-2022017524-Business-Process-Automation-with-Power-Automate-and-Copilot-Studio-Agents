#!/usr/bin/env python3
"""
LU3 Activity 3 — Task 1: load the 20 course brochures into Pinecone.

This is the INGESTION half of RAG. It runs ONCE. After it, the brochures live in
Pinecone as vectors and the Copilot Studio flow only ever reads them.

What it does, in order:

  1. Creates a serverless index with an INTEGRATED embedding model
     (llama-text-embed-v2, 1024 dimensions). "Integrated" means Pinecone embeds
     the text server-side — you upload words, not numbers.
  2. Waits for the index to become Ready.
  3. Uploads all 20 brochures, one record each, WHOLE (no chunking).
  4. Verifies: counts the vectors, then runs three real searches.

Usage:

    export PINECONE_API_KEY=pcsk_...        # from app.pinecone.io
    python3 ingest_brochures.py

    python3 ingest_brochures.py --recreate  # delete and rebuild from scratch

Requires only the Python standard library.
"""

import argparse
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.request

# ----------------------------------------------------------------- settings
INDEX_NAME = "cookbake-brochures"
EMBED_MODEL = "llama-text-embed-v2"   # Pinecone-hosted. 1024 dims, 2048-token limit.
TEXT_FIELD = "chunk_text"             # MUST match field_map below and the upload records
NAMESPACE = "__default__"             # the default namespace, spelled out for the URL
CLOUD, REGION = "aws", "us-east-1"
API_VERSION = "2025-04"

HERE = os.path.dirname(os.path.abspath(__file__))
BROCHURES = os.path.join(HERE, "brochures")

KEY = os.environ.get("PINECONE_API_KEY", "").strip()
if not KEY:
    sys.exit("PINECONE_API_KEY is not set.\n"
             "  export PINECONE_API_KEY=pcsk_...   (get one at app.pinecone.io)")


def call(url, method="GET", body=None, ctype="application/json", raw=False):
    """One tiny HTTP helper so every request carries the same three headers."""
    data = body if raw else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Api-Key": KEY,
        "Content-Type": ctype,
        "X-Pinecone-Api-Version": API_VERSION,
    })
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return r.status, (json.loads(txt) if txt.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


# ------------------------------------------------------------------- step 1
def create_index(recreate=False):
    status, existing = call(f"https://api.pinecone.io/indexes/{INDEX_NAME}")

    if status == 200 and recreate:
        print(f"  deleting existing index '{INDEX_NAME}' …")
        call(f"https://api.pinecone.io/indexes/{INDEX_NAME}", method="DELETE")
        time.sleep(8)
        status = 404

    if status == 200:
        host = existing["host"]
        embed = existing.get("embed") or {}
        print(f"  index '{INDEX_NAME}' already exists")
        print(f"    dimension : {existing['dimension']}")
        print(f"    embedding : {embed.get('model', 'NONE — you would supply vectors')}")
        if not embed:
            sys.exit("\n  This index has NO integrated embedding model, so it expects\n"
                     "  raw vectors. Re-run with --recreate to rebuild it correctly.")
        return host

    print(f"  creating '{INDEX_NAME}' with integrated embedding …")
    status, body = call(
        "https://api.pinecone.io/indexes/create-for-model",
        method="POST",
        body={
            "name": INDEX_NAME,
            "cloud": CLOUD,
            "region": REGION,
            # This block is the embedding configuration. field_map tells Pinecone
            # WHICH field of each uploaded record to embed. Get the name wrong and
            # records are stored with NO vector and NO error.
            "embed": {
                "model": EMBED_MODEL,
                "field_map": {"text": TEXT_FIELD},
            },
        })
    if status not in (200, 201):
        sys.exit(f"  create failed ({status}): {body}")

    print(f"    dimension : {body['dimension']}      <- chosen by the model, not by you")
    print(f"    embedding : {body['embed']['model']}")
    print(f"    metric    : {body['metric']}")
    return body["host"]


def wait_ready():
    for _ in range(40):
        _, b = call(f"https://api.pinecone.io/indexes/{INDEX_NAME}")
        if b.get("status", {}).get("state") == "Ready":
            return
        time.sleep(3)
    sys.exit("  index never became Ready")


# ------------------------------------------------------------------- step 2
def upload(host):
    files = sorted(glob.glob(os.path.join(BROCHURES, "*.txt")))
    if not files:
        sys.exit(f"  no .txt files found in {BROCHURES}")

    lines, longest = [], 0
    for path in files:
        name = os.path.basename(path)
        code = name.split("_")[0]                      # BAK-101_artisan… -> BAK-101
        text = open(path, encoding="utf-8").read()
        longest = max(longest, len(text))
        # ONE RECORD PER BROCHURE, WHOLE. This is the chunking decision, and it is
        # the single most consequential setting in the system. See the README.
        lines.append(json.dumps({
            "_id": code,
            TEXT_FIELD: text,          # <- the field Pinecone embeds
            "source": name,            # <- everything else becomes filterable metadata
            "course_code": code,
        }))

    print(f"  {len(lines)} brochures, longest {longest} characters "
          f"(~{longest // 4} tokens — well under the model's 2048 limit)")

    # NDJSON: one JSON object per line. No wrapping array, no commas between lines.
    payload = ("\n".join(lines) + "\n").encode()
    status, body = call(f"https://{host}/records/namespaces/{NAMESPACE}/upsert",
                        method="POST", body=payload,
                        ctype="application/x-ndjson", raw=True)
    if status not in (200, 201):
        sys.exit(f"  upload failed ({status}): {body}")
    print(f"  uploaded — HTTP {status}")


# ------------------------------------------------------------------- step 3
def verify(host):
    time.sleep(8)  # the index is eventually consistent; give it a moment

    _, stats = call(f"https://{host}/describe_index_stats", method="POST", body={})
    counts = {(k or "(default)"): v["vectorCount"]
              for k, v in stats.get("namespaces", {}).items()}
    print(f"  vectors in index: {counts}")
    if stats.get("totalVectorCount") != 20:
        print("  ⚠️  expected 20 — check for upload errors above")

    print("\n  three test searches:\n")
    for q in ["How much is the sourdough course?",
              "Do you have beginner cooking courses?",
              "Do you offer a Vietnamese pho cooking course?"]:
        status, body = call(
            f"https://{host}/records/namespaces/{NAMESPACE}/search",
            method="POST",
            body={"query": {"inputs": {"text": q}, "top_k": 3},
                  "fields": ["course_code", TEXT_FIELD]})
        if status != 200:
            print(f"    search failed ({status}): {body}")
            continue
        hits = body["result"]["hits"]
        print(f"    Q: {q}")
        for h in hits:
            f = h["fields"]
            fee = next((l.strip() for l in f[TEXT_FIELD].split("\n") if "Fee" in l), "")
            print(f"       {h['_score']:.3f}  {f['course_code']:<9} {fee}")
        print()


# ---------------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--recreate", action="store_true",
                    help="delete the index first and rebuild it")
    args = ap.parse_args()

    print("\nSTEP 1  Create the index (integrated embedding)")
    host = create_index(recreate=args.recreate)
    wait_ready()
    print(f"  host: {host}\n")

    print("STEP 2  Upload the brochures as TEXT")
    upload(host)
    print()

    print("STEP 3  Verify")
    verify(host)

    print("Done. Paste this URL into your flow's HTTP node:\n")
    print(f"  https://{host}/records/namespaces/{NAMESPACE}/search\n")
