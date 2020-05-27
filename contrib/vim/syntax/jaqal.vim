if exists("b:current_syntax")
    finish
endif

" Add angle brackets to matchpairs (for using % and syntax highlighting)
set mps+=<:>


" GetInstances is a helper function to parse the file and search for regexstr,
" matching occurences are then added to syntaxClass. This will then highlight
" subsequent references to a previous variable with its appropriate type.
" It seems this functionality doesn't exist natively in vimscript.
function! GetInstances(regexstr, syntaxClass)
    try
        silent exe "vimgrep /" . a:regexstr . "/j %"
    catch /^Vim\%((\a\+)\)\=:E480/ " no match
      " do nothing
    endtry
    let varnames = split(join(map(copy(getqflist()), 'matchlist(v:val.text, a:regexstr)[1]')))
    exe "syn match " . a:syntaxClass . " \"\\<\\(" . join(varnames, '\|') . "\\)\\>\""
endfunction

" Use gate pulse file path information and valid gate names to contruct tag file
" Note: Tag file does not appear to work with gd or gD, but works with
" <Ctrl>-] as well as <Ctrl>-t to jump back.
function! GenerateTag(input, path)
  return a:input . "\t" . a:path . ".py" . "\t" . "/def gate_" . a:input
endfunction


" Grab the path/file used in the usepulses statement and extract all of the
" gate names. This requires a couple variations on GetInstances and is thus
" done manually. Currently grabs all gate_XXX names and is not class-specific
let importstmt = '^\s*from\s*\([^ ]*\)\s*usepulses\s*\*'
let gateblockinit = 'def gate_.*'
let gateblock = "gate_\\(\[^(\]*\\)"

try
  silent exe "vimgrep /" . importstmt . "/j %"
  let importpath = join(split(map(copy(getqflist()), 'matchlist(v:val.text, importstmt)[1]')[0], '\.')[:-2], '/')
  silent exe "vimgrep /" . gateblockinit . "/j " . importpath . ".py"
  let gatevars = split(join(map(copy(getqflist()), 'matchlist(v:val.text, gateblock)[1]')))
  exe "syn match jaqalGate \"\\<\\(" . join(gatevars, '\|') . "\\)\\>\""
  let taglist = map(sort(gatevars), 'GenerateTag(v:val, importpath)')
  " comment out next line to skip generating tags file
  call writefile(taglist, "tags")
catch /^Vim\%((\a\+)\)\=:E480/ " no match
  " do nothing
endtry


" Grab all let/map/macro declarations and store them as keywords
call GetInstances('let\s*\(\S*\)\s.*',    'jaqalLetParamName')
call GetInstances('map\s*\(\S*\)\s.*',    'jaqalMapName')
call GetInstances('macro\s*\(\S*\)\s.*',  'jaqalMacroName')
call GetInstances('register\s*\(\h\w*\)', 'jaqalRegName')


" Define keywords (syn is short for syntax)
syn keyword jaqalKeyword        let nextgroup=jaqalLetParamName skipwhite
syn keyword jaqalRegister       register nextgroup=jaqalRegDelcaration skipwhite
syn keyword jaqalMap            map nextgroup=jaqalMapDeclaration
syn keyword jaqalImport         from usepulses
syn keyword jaqalRepeat         loop
syn keyword jaqalStatement      macro nextgroup=jaqalFunction skipwhite

" counterparts for keyword nextgroup arguments
syn match   jaqalFunction       "\h\w*" display contained
syn match   jaqalMapDeclaration "\s*\h\S*" nextgroup=jaqalRegName skipwhite display contained
syn match   jaqalMapName        "\h\w*" display contained
syn match   jaqalRegDeclaration "\h\w*" display contained
syn match   jaqalMacroName      "\h\w*" display contained
syn match   jaqalLetParamName   "\h\w*" display contained

" Only define syntax highlighting rules for brackets/braces, not regions
syn match   jaqalBracket        "[\<\>|\{\}]\+"
syn match   jaqalRange          "[\[\]]\+"

" Both line/block comments. Support comment folding.
syn match  jaqalComment         "\v//.*$"
syn region jaqalBlockComment    matchgroup=jaqalCommentStart start="/\*" end="\*/" fold extend

"hi def link is equivalent to highlight default link
hi def link jaqalGate           Type
hi def link jaqalComment        Comment
hi def link jaqalKeyword        Keyword
hi def link jaqalRegister       Keyword
hi def link jaqalMap            Keyword
hi def link jaqalRepeat         Repeat
hi def link jaqalFunction       Function
hi def link jaqalStatement      Statement
hi def link jaqalImport         Include
hi def link jaqalRegName        Identifier
hi def link jaqalRegDeclaration Identifier
hi def link jaqalMapName        Identifier
hi def link jaqalMapDeclaration Identifier
hi def link jaqalMacroName      Function
hi def link jaqalLetParamName   Constant
hi def link jaqalBracket        Define
hi def link jaqalRange          Special
hi def link jaqalBlockComment   Comment

let b:current_syntax = "jaqal"
