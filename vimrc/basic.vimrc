" ===========================================
"  Basic Settings
" ===========================================
set nocompatible
filetype plugin indent on
syntax enable

" Encoding
scriptencoding utf-8
set encoding=utf-8

" Timing
set timeout
set ttimeout
set timeoutlen=1000
set ttimeoutlen=100

" Search
set hlsearch
set incsearch
set ignorecase
set smartcase

" Display
set wrap
set cursorline
set ruler
set number
set wildmenu
set showcmd
set laststatus=2
set signcolumn=yes
set scrolloff=5
set display=lastline

" Indentation
set autoindent
set smartindent
set shiftwidth=2
set softtabstop=2
set tabstop=2
set expandtab

" Editing
set backspace=indent,eol,start
set clipboard=unnamed
set hidden
set autoread
set confirm

" Invisible characters
set list
set listchars=tab:>-,trail:-,extends:>,precedes:<,nbsp:%

" Cursor shape: bar in insert mode, block in normal mode
let &t_SI = "\e[6 q"
let &t_EI = "\e[2 q"

" ===========================================
"  Plugin Manager (vim-plug)
" ===========================================
call plug#begin('~/.vim/plugged')

" -- File Explorer --
Plug 'preservim/nerdtree'

" -- Status Line --
Plug 'itchyny/lightline.vim'

" -- Git --
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'

" -- Editing Helpers --
Plug 'tpope/vim-surround'
Plug 'tpope/vim-commentary'
Plug 'jiangmiao/auto-pairs'
Plug 'editorconfig/editorconfig-vim'
Plug 'bronson/vim-trailing-whitespace'

" -- Fuzzy Finder --
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" -- Color Scheme --
Plug 'w0ng/vim-hybrid'
Plug 'morhetz/gruvbox'

" -- Language Support --
Plug 'fatih/vim-go', { 'for': 'go', 'do': ':GoUpdateBinaries' }
Plug 'rust-lang/rust.vim', { 'for': 'rust' }
Plug 'leafgarland/typescript-vim', { 'for': 'typescript' }
Plug 'plasticboy/vim-markdown', { 'for': 'markdown' }
Plug 'elixir-lang/vim-elixir', { 'for': 'elixir' }
Plug 'dart-lang/dart-vim-plugin', { 'for': 'dart' }

" -- Web Development --
Plug 'othree/html5.vim'
Plug 'hail2u/vim-css3-syntax'

" -- Utility --
Plug 'tyru/open-browser.vim'

call plug#end()

" ===========================================
"  NERDTree
" ===========================================
let g:NERDTreeShowHidden = 1
let g:NERDTreeDirArrowExpandable = '+'
let g:NERDTreeDirArrowCollapsible = '-'

map <C-n> :NERDTreeToggle<CR>

" Close vim if NERDTree is the only window left
autocmd BufEnter * if winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

" ===========================================
"  Lightline
" ===========================================
set ambiwidth=single
let g:lightline = {
      \  'colorscheme': 'wombat',
      \  'active': {
      \     'left': [ ['mode', 'paste'], ['fugitive', 'filename', 'modified'] ],
      \     'right': [ ['lineinfo'], ['percent'], ['fileformat', 'fileencoding', 'filetype'] ]
      \  },
      \  'inactive': {
      \     'left': [ ['fugitive', 'filename', 'modified'] ],
      \     'right': [ ['lineinfo'], ['percent'] ]
      \  },
      \  'component_function': {
      \     'fugitive': 'LightlineFugitive',
      \  }
      \ }

function! LightlineFugitive()
  if exists('*FugitiveHead')
    let branch = FugitiveHead()
    return branch !=# '' ? "\u2387 " . branch : ''
  endif
  return ''
endfunction

" ===========================================
"  fzf
" ===========================================
nnoremap <C-p> :Files<CR>
nnoremap <Leader>b :Buffers<CR>
nnoremap <Leader>g :Rg<CR>

" ===========================================
"  Go Settings
" ===========================================
autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4
let g:go_highlight_functions = 1
let g:go_highlight_methods = 1
let g:go_highlight_fields = 1
let g:go_highlight_types = 1
let g:go_highlight_operators = 1
let g:go_highlight_build_constraints = 1
let g:go_fmt_command = 'goimports'

" ===========================================
"  Markdown
" ===========================================
let g:vim_markdown_folding_disabled = 1

" ===========================================
"  Makefile
" ===========================================
autocmd FileType make setlocal noexpandtab tabstop=4 shiftwidth=4

" ===========================================
"  Filetype Detection
" ===========================================
augroup filetypedetect
  autocmd!
  autocmd BufRead,BufNewFile *.md set filetype=markdown
  autocmd BufRead,BufNewFile *.mjs set filetype=javascript
  autocmd BufRead,BufNewFile *.slim,*.slime setfiletype slim
  autocmd BufRead,BufNewFile *.yml,*.yaml set filetype=yaml
augroup END

" ===========================================
"  Open URL under cursor
" ===========================================
function! OpenLink()
  let s:uri = matchstr(getline('.'), '[a-z]*:\/\/[^ >,;:]*')
  if s:uri != ''
    silent exec '!open ' . shellescape(s:uri)
  endif
endfunction
map <Leader>w :call OpenLink()<CR>

" ===========================================
"  Trailing Whitespace
" ===========================================
" Remove trailing whitespace on save (except markdown)
autocmd BufWritePre * if &filetype !=# 'markdown' | :%s/\s\+$//ge | endif
