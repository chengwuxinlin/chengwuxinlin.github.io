\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/03/09 Minimal resume class]

\LoadClass[11pt]{article}

\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage{hyperref}
\RequirePackage{xcolor}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.25em}
\setlist[itemize]{leftmargin=1.4em, itemsep=0.15em, topsep=0.15em}
\hypersetup{
	colorlinks=true,
	urlcolor=blue
}

\makeatletter
\newcommand{\@resumeName}{}
\newcommand{\@resumeAddresses}{}

\newcommand{\name}[1]{\gdef\@resumeName{#1}}
\newcommand{\address}[1]{%
	\ifx\@resumeAddresses\@empty
		\gdef\@resumeAddresses{#1}%
	\else
		\g@addto@macro\@resumeAddresses{\\#1}%
	\fi
}

\AtBeginDocument{%
	\begin{center}
		{\fontsize{22}{24}\selectfont\bfseries \@resumeName\par}
		\vspace{0.35em}
		{\small \@resumeAddresses\par}
	\end{center}
	\vspace{0.7em}
}
\makeatother

\newenvironment{rSection}[1]{%
	\par\vspace{0.9em}
	{\large\bfseries #1\par}
	\vspace{0.35em}
	\hrule
	\vspace{0.55em}
	\begin{list}{}{%
		\setlength{\leftmargin}{0pt}%
		\setlength{\rightmargin}{0pt}%
		\setlength{\labelwidth}{0pt}%
		\setlength{\labelsep}{0pt}%
		\setlength{\itemindent}{0pt}%
		\setlength{\listparindent}{0pt}%
		\setlength{\parsep}{0pt}%
		\setlength{\topsep}{0pt}%
		\setlength{\itemsep}{0.55em}%
	}
}{%
	\end{list}
}
