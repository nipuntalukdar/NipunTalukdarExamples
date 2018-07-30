set expandtab
set ts=4
set tags=/home/nipun/colortokens/ct-lgm/lgm/tags
fixdel
set backspace=indent,eol,start
set smartindent
set autoindent
set hls
syn on

function PythonSettings()
   set tabstop=4
   set softtabstop=4
   set shiftwidth=4
   set textwidth=80
   set expandtab
   set autoindent
   set fileformat=unix
endfunction()

au BufNewFile,BufRead *.py  call PythonSettings()
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
set nu
