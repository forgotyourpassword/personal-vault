---
tags:
  - family
  - chores
  - allowance
  - printable
---

# Printable Chore Log

Quartz: http://192.168.1.223:8080/10-Areas/Family/Printable-Chore-Log

Print the PDF in **landscape** and hang it up. Kids write the date and initials after a parent says the chore is done. Payment is based on checked entries.

- PDF: [[Family Chore Log.pdf]]

<style>
@media print {
  @page { size: Letter landscape; margin: 0.25in; }
  body { background: white !important; }
  .page-title, .breadcrumb-container, footer, .sidebar, .explorer, .toc, .graph, .backlinks, .popover-hint { display: none !important; }
  .chore-log-print { page-break-inside: avoid; break-inside: avoid; }
}
.chore-log-print {
  font-family: Arial, Helvetica, sans-serif;
  color: #111;
  background: white;
  max-width: 10.5in;
  margin: 0 auto;
}
.chore-log-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 2px solid #111;
  padding-bottom: 6px;
  margin-bottom: 6px;
}
.chore-log-header h2 { margin: 0; font-size: 24px; }
.chore-log-note { font-size: 11px; margin-top: 2px; }
.chore-log-meta { font-size: 12px; line-height: 1.5; min-width: 2.6in; }
.chore-log-line { display:inline-block; border-bottom:1px solid #111; min-width:1.15in; height:14px; }
.chore-log-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.chore-log-table th, .chore-log-table td { border: 1px solid #111; }
.chore-log-table th { background: #eee; font-size: 10px; line-height: 1.05; padding: 3px 2px; }
.chore-log-table th span { font-size: 8.5px; font-weight: 400; }
.chore-log-table td { height: 34px; vertical-align: top; }
.chore-log-table .chore { width: 2.45in; font-size: 10.5px; font-weight: 700; padding: 4px 5px; }
.chore-log-table .price { width: .45in; text-align: center; font-size: 14px; font-weight: 800; padding-top: 8px; }
.chore-log-table .slot { width: 1.05in; }
.chore-log-table .slotcell { font-size: 9px; line-height: 1.35; padding: 2px 4px; }
.chore-log-table .slotcell div:first-child { border-bottom: 1px solid #aaa; min-height: 15px; }
.chore-log-footer { display: grid; grid-template-columns: 1.45fr 1fr; gap: 10px; margin-top: 7px; }
.chore-log-box { border: 1px solid #111; padding: 6px 8px; min-height: 54px; }
.chore-log-box h3 { margin: 0 0 3px; font-size: 12px; }
.chore-log-box p { margin: 2px 0; font-size: 10.5px; line-height: 1.25; }
.chore-log-totals { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; font-size: 10.5px; }
.chore-log-blank { display:inline-block; border-bottom:1px solid #111; min-width:.55in; height:12px; }
</style>

<div class="chore-log-print">
  <div class="chore-log-header">
    <div>
      <h2>Family Chore Log</h2>
      <div class="chore-log-note">Parent checks first. Then write date + initials. No check, no payout.</div>
    </div>
    <div class="chore-log-meta">
      Week of: <span class="chore-log-line"></span><br>
      Parent initials: <span class="chore-log-line"></span>
    </div>
  </div>

  <table class="chore-log-table">
    <thead>
      <tr><th class="chore">Chore</th><th class="price">Pay</th><th class="slot">Done 1<br><span>Date / Initials</span></th><th class="slot">Done 2<br><span>Date / Initials</span></th><th class="slot">Done 3<br><span>Date / Initials</span></th><th class="slot">Done 4<br><span>Date / Initials</span></th><th class="slot">Done 5<br><span>Date / Initials</span></th><th class="slot">Done 6<br><span>Date / Initials</span></th></tr>
    </thead>
    <tbody>
      <tr><td class="chore">Bathroom supply reset</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Clean master bathroom</td><td class="price">$5</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Clean kids bathroom</td><td class="price">$5</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Clean powder room</td><td class="price">$3</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Vacuum and mop first level floor</td><td class="price">$5</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Clean toys off basement floor</td><td class="price">$2</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Vacuum and mop basement floor</td><td class="price">$5</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Daily empty litter boxes</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Vacuum upstairs hallway carpets</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Empty small trash cans around the house</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Take kitchen trash bag to outside bin</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Load dishwasher</td><td class="price">$2</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Unload dishwasher</td><td class="price">$2</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Wipe kitchen counters</td><td class="price">$2</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr><tr><td class="chore">Refill pet water bowls</td><td class="price">$1</td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td><td class="slotcell"><div>Date:</div><div>Init:</div></td></tr>
    </tbody>
  </table>

  <div class="chore-log-footer">
    <div class="chore-log-box">
      <h3>Tally rule</h3>
      <p>For each kid: count their initials on each chore row × the listed price. Example: 3 dishwasher unloads × $2 = $6.</p>
    </div>
    <div class="chore-log-box">
      <h3>Amount owed</h3>
      <div class="chore-log-totals">
        <div>Connor<br>$ <span class="chore-log-blank"></span></div>
        <div>Madison<br>$ <span class="chore-log-blank"></span></div>
        <div>McKenzie<br>$ <span class="chore-log-blank"></span></div>
      </div>
    </div>
  </div>
</div>

Related: [[Chores and Activities List]]

Quartz: http://192.168.1.223:8080/10-Areas/Family/Printable-Chore-Log
