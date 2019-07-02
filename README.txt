Hi Drew!

Just a quick readme/some comments.
I used a library called BeautifulSoup which parses HTML and allows me to get the img and a tags easily, you can install this with 'pip install beautifulsoup4'
To run the file, just use python3 site_map.py and follow the instructions!
The file will be outputed to a result.json file in the same directory

I was going over the 3 hour mark and didn't have time to refactor it using parallelization. If I did, I would probably change line 17, "for url in urls" into normal for loop with indexing, and divide the work into 2 or 4 partitions, and merge the results afterwards. I would refactor the work inside that loop inside a function as well.

Let me know if you have any questions, thanks! 