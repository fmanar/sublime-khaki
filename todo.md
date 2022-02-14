## Todo Items
- engage/disengage command mode, done
- add hl, done
- add HL, done
- add jk, done
- add JK, done

- filters: don't return empty regions

- ia
- repetitions
- ftFT, backwards?
- w W a-w: words, WORDS, sub-words, b, e
- select-all

- shrink selection to current (what is kak word?), cycle current, uh how to even display current?
- shrink selections to caret
- change direction
- orient selections
- rotate
- align
- split to lines
- add next occurance of selection
- extend cursor down, but not by line -> visual box
- trim (whitespace), split on whitespace

- dissallow empty selections in command mode, need to manage mouse input
- refactor select/remove/keep/drop into single command with option
  - close, has better class structure
  - separate into interactive command and one go
- limit motions to valid file locations
- change regex command to use sequential find next? better for large files but maybe not when selection is the whole file anyway
- menu style commands
- wasd style map?  kinda awkward in brief test

## historical ideas

review sam lit, what were the 4 commands?
- select/remove
- keep/drop selections with regex

- what about an extend/add?
- selection set operations? a, b, a-b, b-a, union, intersection

## other verbs

select: choose, cull, elect, pick, take, mark, tag, tap, winnow, where
remove: eliminate, erase, exclude, obliterate, purge, block, ignore, omit, reject, separate, kill
keep: preserve, pick, retain, save, where, with, include,
drop: cancel, lose, dismiss, delete, kick, kill

test command start, select other, cancel/continue