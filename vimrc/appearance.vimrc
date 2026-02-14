" ===========================================
"  Appearance Settings
" ===========================================
set background=dark

" Use 24-bit true color if terminal supports it
if has('termguicolors')
  set termguicolors
endif

" Apply colorscheme (installed via vim-plug in basic.vimrc)
silent! colorscheme hybrid
