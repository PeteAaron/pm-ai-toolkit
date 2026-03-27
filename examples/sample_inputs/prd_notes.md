# Product Notes: Export to PDF

## Background

Enterprise customers keep asking for the ability to export reports as PDFs.
It comes up almost every week on customer calls.

Currently, the only way to share a report is to share a live link, which requires
the recipient to have a product login. Most stakeholders at our customers' companies
(finance, legal, execs) don't have accounts and won't create one just to view a report.

## Who is asking

Mostly analysts and ops managers at mid-market and enterprise accounts.
They want to share weekly/monthly snapshots with their internal stakeholders —
people who don't use the product and never will.

A few customers have tried screenshotting reports, but that breaks formatting
and loses the data tables. Not a real solution.

## What we think they need

A "Download as PDF" button on any report view.
PDF should preserve the layout, charts, and data tables.
Should include the report title, date range, and a footer with the account name.
No interactivity needed — just a clean snapshot.

## Constraints and open questions

We haven't decided whether this should be a premium feature or available to all plans.
That's a pricing/packaging question that needs a decision from Marcus and the commercial team.

There's also a question about file size — some reports have large data tables.
We don't know yet if there's a storage or delivery concern.

Mobile layout for reports is still being designed. Should the PDF export wait for that,
or do we ship web-only first and add mobile later?

## Why now

Three enterprise customers flagged it on calls this week.
One of them is up for renewal in May and export is on their list of must-haves.
