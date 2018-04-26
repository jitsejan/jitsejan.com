Title: Latex cheatsheet
Date: 2017-03-26 16:45
Modified: 2017-03-26 16:45
Category: Latex
Tags: latex, cheatsheet
Slug: latex-cheatsheet
Authors: Jitse-Jan
Summary: This is my Latex cheatsheet

This is my [Latex](https://www.latex-project.org/) cheatsheet

## Add style to a code listing
**styles.tex**
``` latex
\definecolor{dkgreen}{rgb}{0,0.6,0}
\definecolor{gray}{rgb}{0.5,0.5,0.5}
\definecolor{mauve}{rgb}{0.58,0,0.82}
\definecolor{light-gray}{gray}{0.25}

\usepackage{listings}

\lstdefinestyle{java}{
  language=Java,
  aboveskip=3mm,
  belowskip=3mm,
  showstringspaces=false,
  columns=flexible,
  basicstyle={\footnotesize\ttfamily},
  numberstyle={\tiny},
  numbers=left,
  keywordstyle=\color{blue},
  commentstyle=\color{dkgreen},
  stringstyle=\color{mauve},
  breaklines=true,
  breakatwhitespace=true,
  tabsize=3,
}
```
**main.tex**
``` latex
\input{styles.tex}
\lstinputlisting[style=Java, frame=single, caption={Hello world}, captionpos=b]{helloworld.java}
```
Bonus: rename the caption from _Listing_ to _Code snippet_ with the following:
``` latex
\renewcommand*\lstlistingname{Code snippet}
```

## Subfigures
``` latex
\usepackage{graphicx}
\usepackage{caption}
\usepackage{subcaption}

\begin{figure*}[h]
    \centering
    \begin{subfigure}[t]{0.5\textwidth}
        \centering
        \includegraphics[width=2.2in]{image_one.png}
        \caption{Image one}
    \end{subfigure}%
    ~ 
    \begin{subfigure}[t]{0.5\textwidth}
        \centering
        \includegraphics[width=2.2in]{image_two.png}
        \caption{Image two}
    \end{subfigure}
    \caption{These are two images}
\end{figure*}
```
