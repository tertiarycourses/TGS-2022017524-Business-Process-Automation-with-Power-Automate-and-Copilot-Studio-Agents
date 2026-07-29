import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.join(repo, "outputs", "019f936b-fb73-7731-b12e-c8843dd59814");

async function buildWorkbook({fileName, sheetName, tableName, headers, widths}) {
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add(sheetName);
  sheet.getRange(`A1:${String.fromCharCode(64 + headers.length)}2`).values = [
    headers,
    headers.map(() => ""),
  ];
  const header = sheet.getRange(`A1:${String.fromCharCode(64 + headers.length)}1`);
  header.format = {
    fill: "#1769E0",
    font: { bold: true, color: "#FFFFFF" },
    rowHeight: 28,
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
  sheet.getRange(`A2:${String.fromCharCode(64 + headers.length)}2`).format = {
    fill: "#F3F7FC",
    rowHeight: 24,
  };
  widths.forEach((width, index) => {
    const column = String.fromCharCode(65 + index);
    sheet.getRange(`${column}:${column}`).format.columnWidth = width;
  });
  sheet.freezePanes.freezeRows(1);
  const table = sheet.tables.add(
    `A1:${String.fromCharCode(64 + headers.length)}2`,
    true,
    tableName,
  );
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = true;
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 1.5,
    format: "png",
  });
  await fs.writeFile(
    path.join(out, fileName.replace(".xlsx", ".png")),
    new Uint8Array(await preview.arrayBuffer()),
  );
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(path.join(out, fileName));
  const inspection = await workbook.inspect({
    kind: "table",
    range: `${sheetName}!A1:${String.fromCharCode(64 + headers.length)}3`,
    tableMaxRows: 3,
    tableMaxCols: headers.length,
  });
  console.log(fileName, inspection.ndjson);
}

await fs.mkdir(out, { recursive: true });
await buildWorkbook({
  fileName: "Enquiry Log.xlsx",
  sheetName: "Enquiries",
  tableName: "EnquiryLog",
  headers: ["Timestamp", "Name", "Email", "Tel", "Message", "Status", "Source"],
  widths: [22, 20, 30, 16, 42, 16, 24],
});
await buildWorkbook({
  fileName: "Event Log.xlsx",
  sheetName: "Registrations",
  tableName: "EventLog",
  headers: ["Timestamp", "Name", "Email", "Tel", "JoiningEvent", "NotificationSent", "Notes"],
  widths: [22, 20, 30, 16, 18, 22, 40],
});
