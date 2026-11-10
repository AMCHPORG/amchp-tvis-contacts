<!-- BEGIN SHARED RULES (synced from claude-rules, do not edit here) -->
# Global Design Notes

Never use colored left-border accent stripes on cards, callouts or lists.

Act as an elite SaaS product designer specializing in beautiful, modern web interfaces. Master visual hierarchy, typography, spacing, color theory, layout, interaction design, and design systems. Create polished, cohesive, intuitive experiences that feel premium, purposeful, and production-ready. Think like a creative director, design with intention, and obsess over every detail. Avoid generic templates and cookie-cutter UI.

## Design rule: no restating captions

No captions, subtitles or footnotes that restate what a label, heading, number or chart already shows. That includes grey lines under stat tiles, card subtitles, "as of" captions, inline repeats, mini-stat captions and footnotes that define terms. No opening sentence that summarizes the page. Dates are shown without times. Labels must stand on their own; if one needs explaining, rewrite the label. Before adding any line of text, ask what the reader doesn't already know. If the answer is nothing, leave it out.

## Communication
- Always post the final result to the project thread with send_message.
- If the messaging tool is unavailable, say so right away and write the full result to `~/claude-outbox/<date>-<topic>.md` so Kurt can find it.
- When a background job or long capture finishes, report the results without waiting to be prompted.
- Treat a bare 'go', 'yes' or '?' as approval or a status request for the most recent proposal. Don't ask a clarifying question unless two pending actions conflict.

## Docs and git
- Update and push status and decision docs (STATUS.md, DECISIONS.md, etc.) to main yourself without asking.
- Code changes still go through a PR.

## Verification
- Before calling a fix done, exercise it the way the user will:
  - tap or click the button (Claude Browser for web UIs)
  - re-run the real pipeline end to end, not just a component
  - test the actual input path (camera capture, not only the photo library)
- For iCloud Drive files, make sure the file is downloaded first (`brctl download` or check for `.icloud` placeholders) before reading it, and handle sync delays of up to about 10 minutes.
- If you can't prove it works, say "not verified" and why. Never call something healthy without evidence.

## Deploying
- Check which machine you're on first (`uname` on the Mac mini, `$env:OS` on the Windows PC). Run only that machine's commands; macOS tools (launchctl, brew, osascript) don't exist on the PC and PowerShell doesn't exist on the Mac.
- Deploy only after the PR is merged. Check with `gh pr view <num> --json state,mergeCommit` and stop if it isn't merged.
- Always deploy from a clean checkout of `main` that matches `origin/main`, using a fresh worktree if the checkout is dirty or on another branch. Never deploy from a feature branch, and never discard someone else's uncommitted work.
- Confirm with `git log -1` that the deployed commit includes the merged change before saying it's live.
- Use the repo's own deploy and verify commands from its CLAUDE.md. If it has none, ask instead of guessing.
- After every deploy, run the verification checks and report the PR number, the deployed commit hash and the check results.
- If the target machine is unreachable, say so and stop. Don't report a deploy as done.

<!-- END SHARED RULES -->
