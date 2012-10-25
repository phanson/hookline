      /\    H  H  OO   OO  K  K L    III N   N EEEE
      \/    H  H O  O O  O K K  L     I  NN  N E
      ||    HHHH O  O O  O KK   L     I  N N N EEE
      ||    H  H O  O O  O K K  L     I  N  NN E
    \_/\_/  H  H  OO   OO  K  K LLLL III N   N EEEE

## Purpose

This is a little utility I wrote for myself. It scrapes a specific web page that has a predictable format for scheduling volunteer activities and produces a Python data structure that can be manipulated and queried for analysis, logging, automatic calendar synchronization, etc.

It is not a generalized schedule scraper, nor am I interested in that project. However, the HookLine code is available for people who are interested in adapting it or using it as an example for writing their own, similar, utilities.

## Dependencies

HookLine requires the following external Python libraries:

* [FeedParser](http://code.google.com/p/feedparser/)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

It's tested running under Python 3.1, and there are no plans to expand testing.

## Name

Since this is project just for me personally, I went with a silly name and justified it later. Think of it like this: an entry in a schedule that says you have to do something is the _line_ that puts you "on the hook" - the _hook line_.

It also sets up a name for the calendar synchronization part, "hook line and syncer". (I may love bad puns too much.)
