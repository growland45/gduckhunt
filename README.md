This Python 3 script uses urllib and htmlparse to scrape search results from DuckDuckGo, and uses tkinter to present the results with buttons to launch entries in a browser. It honors http_proxy. Optionally can pass search keywords on the command line.

Thanks to Eugene Bakin ( https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df ) for working code for a scrollable frame in tkinter. That's harder than it should be.

I looked at ttk but was having trouble getting the palette to work, so fell back to straight tkinter. Always do what you know works.
