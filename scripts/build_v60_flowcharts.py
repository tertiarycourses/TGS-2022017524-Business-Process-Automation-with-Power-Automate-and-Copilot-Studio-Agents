#!/usr/bin/env python3
"""Generate the shared Version 6.0 lab flowcharts used by Labs, LG and PPT."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

LABS = {
    "labs/Day 1/Lab 1 - Forms Email Confirmation/assets": r'''
      form [label="Course Enquiry Form\nName · Email · Tel · Message", fillcolor="#EAF2FF"];
      trigger [label="When a new response\nis submitted"];
      details [label="Get response details"];
      email [label="Send confirmation email\nto submitted Email", fillcolor="#E8F7EE"];
      form -> trigger -> details -> email;
    ''',
    "labs/Day 1/Lab 2 - Forms Enquiry Logging/assets": r'''
      form [label="Course Enquiry Form", fillcolor="#EAF2FF"];
      trigger [label="Form response trigger"];
      details [label="Get response details"];
      excel [label="Add row to EnquiryLog\nin Enquiry Log.xlsx", fillcolor="#E8F7EE"];
      email [label="Send confirmation email", fillcolor="#FFF4E5"];
      form -> trigger -> details -> excel -> email;
    ''',
    "labs/Day 1/Lab 3 - Event Registration Branching/assets": r'''
      form [label="Event Registration Form", fillcolor="#EAF2FF"];
      details [label="Get response details"];
      joining [label="Joining the Event\n= Yes?", shape=diamond, fillcolor="#FFF4E5"];
      yeslog [label="Add Yes row\nto EventLog", fillcolor="#E8F7EE"];
      admin [label="Email participant details\nto administrator", fillcolor="#E8F7EE"];
      nolog [label="Add No row\nto EventLog", fillcolor="#FDECEC"];
      user [label="Email user:\nthanks and next time", fillcolor="#FDECEC"];
      form -> details -> joining;
      joining -> yeslog [label=" YES"]; yeslog -> admin;
      joining -> nolog [label=" NO"]; nolog -> user;
    ''',
    "labs/Day 1/Lab 4 - Leave Approval/assets": r'''
      form [label="Leave Application Form", fillcolor="#EAF2FF"];
      details [label="Get response details"];
      approval [label="Start and wait\nfor an approval", fillcolor="#FFF4E5"];
      outcome [label="Outcome\n= Approve?", shape=diamond, fillcolor="#FFF4E5"];
      approved [label="Email approved result\nto applicant", fillcolor="#E8F7EE"];
      rejected [label="Email rejection + comments\nto applicant", fillcolor="#FDECEC"];
      form -> details -> approval -> outcome;
      outcome -> approved [label=" YES"];
      outcome -> rejected [label=" NO"];
    ''',
    "labs/Day 1/Lab 5 - IT Support Agent/assets": r'''
      teams [label="Employee in Teams", fillcolor="#EAF2FF"];
      agent [label="IT Support Agent\nInstructions + safety", fillcolor="#F1EAFF"];
      faq [label="IT Support FAQ.pdf\nApproved knowledge", fillcolor="#E8F7EE"];
      grounded [label="Grounded answer", fillcolor="#E8F7EE"];
      escalate [label="Service desk escalation", fillcolor="#FFF4E5"];
      teams -> agent; faq -> agent;
      agent -> grounded [label=" supported"];
      agent -> escalate [label=" unsupported / sensitive"];
    ''',
    "labs/Day 1/Lab 6 - HR Support Agent/assets": r'''
      pdf [label="HR Policies.pdf", fillcolor="#EAF2FF"];
      sharepoint [label="SharePoint\nHR Policy Knowledge", fillcolor="#E8F7EE"];
      agent [label="HR Support Agent\nInstructions + privacy", fillcolor="#F1EAFF"];
      teams [label="Employee in Teams", fillcolor="#EAF2FF"];
      answer [label="Grounded policy answer", fillcolor="#E8F7EE"];
      escalate [label="HR / manager escalation", fillcolor="#FFF4E5"];
      pdf -> sharepoint -> agent;
      teams -> agent;
      agent -> answer [label=" supported"];
      agent -> escalate [label=" decision / personal data"];
    ''',
    "labs/Day 1/Lab 7 - Support Request Routing/assets": r'''
      form [label="Support Request Form\nName · Email · Type · Message", fillcolor="#EAF2FF"];
      details [label="Get response details"];
      route [label="Support Type\n= IT Support?", shape=diamond, fillcolor="#FFF4E5"];
      it [label="Run IT Support Agent", fillcolor="#F1EAFF"];
      hr [label="Run HR Support Agent", fillcolor="#F1EAFF"];
      itemail [label="Email IT reply to user", fillcolor="#E8F7EE"];
      hremail [label="Email HR reply to user", fillcolor="#E8F7EE"];
      form -> details -> route;
      route -> it [label=" YES"]; it -> itemail;
      route -> hr [label=" NO"]; hr -> hremail;
    ''',
    "labs/Day 2/Lab 8 - Website HTTP Enquiry/assets": r'''
      rankdir=TB;
      url [label="Learner pastes\nWebhook URL", fillcolor="#FFF4E5"];
      page [label="Enquiry website\nName · Email · Tel · Message", fillcolor="#EAF2FF"];
      post [label="POST JSON"];
      trigger [label="When an HTTP request\nis received", fillcolor="#F1EAFF"];
      email [label="Email administrator", fillcolor="#E8F7EE"];
      response [label="Response 200 + JSON", fillcolor="#E8F7EE"];
      status [label="Show status on page", fillcolor="#EAF2FF"];
      { rank=same; url; page; post; trigger; }
      { rank=same; email; response; status; }
      url -> page; page -> post -> trigger -> email -> response -> status;
    ''',
    "labs/Day 2/Lab 9 - Finance Agent Web Chat/assets": r'''
      rankdir=TB;
      url [label="Learner pastes\nWebhook URL", fillcolor="#FFF4E5"];
      chat [label="Finance chat page\nUser prompt", fillcolor="#EAF2FF"];
      trigger [label="HTTP request trigger"];
      agent [label="Run Finance\nInformation Agent", fillcolor="#F1EAFF"];
      kb [label="Finance Knowledge\nBase.pdf", fillcolor="#E8F7EE"];
      response [label="Response JSON\nreply + disclaimer", fillcolor="#E8F7EE"];
      browser [label="Display reply in chat", fillcolor="#EAF2FF"];
      { rank=same; url; chat; trigger; agent; }
      { rank=same; kb; response; browser; }
      url -> chat; chat -> trigger -> agent -> response -> browser;
      kb -> agent;
    ''',
    "labs/Day 2/Lab 10 - AI Trading Advisor Website/assets": r'''
      rankdir=TB;
      page [label="Trading website\nTradingView + symbol + prompt", fillcolor="#EAF2FF"];
      url [label="Learner-entered\nWebhook URL", fillcolor="#FFF4E5"];
      trigger [label="HTTP request trigger"];
      agent [label="Finance Advisor Agent", fillcolor="#F1EAFF"];
      m1 [label="Twelve Data\n1-minute candles", fillcolor="#E8F7EE"];
      m15 [label="Twelve Data\n15-minute candles", fillcolor="#E8F7EE"];
      h1 [label="Twelve Data\n1-hour candles", fillcolor="#E8F7EE"];
      news [label="NewsAPI\nrecent news", fillcolor="#E8F7EE"];
      synthesis [label="Compare timeframes + news\nstate uncertainty", fillcolor="#F1EAFF"];
      response [label="Response JSON\nanalysis + risk note", fillcolor="#EAF2FF"];
      browser [label="Display analysis + risk note\non trading website", fillcolor="#EAF2FF"];
      { rank=same; url; page; trigger; agent; }
      { rank=same; m1; m15; h1; news; }
      { rank=same; synthesis; response; browser; }
      url -> page; page -> trigger -> agent;
      agent -> m1; agent -> m15; agent -> h1; agent -> news;
      m1 -> synthesis; m15 -> synthesis; h1 -> synthesis; news -> synthesis;
      synthesis -> response -> browser;
    ''',
    "labs/Day 2/Lab 11 - Travel Expense Agent and Agent Flow/assets": r'''
      rankdir=TB;
      staff [label="Staff conversation", fillcolor="#EAF2FF"];
      agent [label="Expense Claim Agent\npolicy knowledge + instructions", fillcolor="#F1EAFF"];
      tool [label="Agent flow tool\nfixed policy checks", fillcolor="#E8F7EE"];
      toolresult [label="Decision + reason + reference", fillcolor="#E8F7EE"];
      form [label="Expense claim form", fillcolor="#EAF2FF"];
      flow [label="Triggered agent flow", fillcolor="#FFF4E5"];
      runagent [label="Run an agent\nstructured review", fillcolor="#F1EAFF"];
      route [label="High-confidence\npolicy-aligned?", shape=diamond, fillcolor="#FFF4E5"];
      normal [label="Normal manager approval", fillcolor="#E8F7EE"];
      human [label="Human exception review", fillcolor="#FDECEC"];
      outcome [label="Claimant receives\nhuman outcome", fillcolor="#EAF2FF"];
      staff -> agent -> tool -> toolresult -> agent;
      form -> flow -> runagent -> route;
      route -> normal [label=" YES"];
      route -> human [label=" NO"];
      normal -> outcome;
      human -> outcome;
    ''',
    "labs/Day 2/Lab 11 - Procurement Request Approval/assets": r'''
      rankdir=LR;
      form [label="Procurement Request Form\nnew response", fillcolor="#EAF2FF"];
      details [label="Get response details\nusing dynamic Response Id", fillcolor="#EAF2FF"];
      approval [label="Start and wait\nfor an approval", fillcolor="#FFF4E5"];
      outcome [label="Check approval outcome", shape=diamond, fillcolor="#F1EAFF"];
      approved [label="Send approval email", fillcolor="#E8F7EE"];
      rejected [label="Send rejection email", fillcolor="#FDECEC"];
      requester [label="Requester receives\nthe human decision", fillcolor="#EAF2FF"];
      form -> details -> approval -> outcome;
      outcome -> approved [label=" APPROVED"];
      outcome -> rejected [label=" REJECTED"];
      approved -> requester;
      rejected -> requester;
    ''',
}

HEADER = r'''digraph G {
  graph [rankdir=LR, bgcolor="white", pad="0.25", nodesep="0.45", ranksep="0.6",
         fontname="Arial", dpi=180];
  node [shape=box, style="rounded,filled", fillcolor="#F5F8FC",
        color="#8FA6C0", penwidth=1.5, fontname="Arial", fontsize=12,
        margin="0.16,0.12"];
  edge [color="#365C82", penwidth=1.7, arrowsize=0.8, fontname="Arial",
        fontsize=10, fontcolor="#365C82"];
'''

for relative, body in LABS.items():
    asset_dir = ROOT / relative
    asset_dir.mkdir(parents=True, exist_ok=True)
    dot_path = asset_dir / "flowchart.dot"
    png_path = asset_dir / "flowchart.png"
    dot_path.write_text(HEADER + body + "\n}\n", encoding="utf-8")
    subprocess.run(
        ["/opt/homebrew/bin/dot", "-Tpng", str(dot_path), "-o", str(png_path)],
        check=True,
    )
    print(png_path)
