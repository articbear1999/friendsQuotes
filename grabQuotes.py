from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def concatQuotes(linesCombined, lines, folderDest):
    for quote in lines:
        try:
            if quote[0] in "([{<":  # if not a quote
                continue
            if ":" in quote:  # if it is a quote
                linesCombined = linesCombined + "\n" + quote
        except IndexError:
            print("error occurred in folderDest: " + folderDest + "\nProbably just a gif at the end")
    return linesCombined


# start logging in using selenium
#ch_options = webdriver.ChromeOptions()

# set default download area as the path you want
#pref = {"download.default_directory": r"C:\Users\Artic\Desktop\Water"}
#ch_options.add_experimental_option("prefs", pref)
browser = webdriver.Chrome()
# go to the transcribed page
browser.get("https://fangj.github.io/friends/")

# get all a elements inside of li elements
epsList = browser.find_elements_by_css_selector("li a")
for episodes in epsList:
    if episodes.text[0] == "1":
        continue
    main_window = browser.current_window_handle
    if episodes.text[3] == " " or episodes.text[3] == "-":
        seas = episodes.text[0]
        epsNum = episodes.text[1] + episodes.text[2]
    else:   # if season ten parse season and episodes over by one
        seas = episodes.text[0] + episodes.text[1]
        epsNum = episodes.text[2] + episodes.text[3]
    episodes.send_keys(Keys.CONTROL + Keys.RETURN)
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    browser.switch_to.window(browser.window_handles[1])
    quoteList = browser.find_elements_by_css_selector("p")
    seasAndEps = r"\s" + seas + "ep" + str(epsNum) + ".txt"
    folderDest = r"C:\Users\Artic\Desktop\friendsQuotes" + seasAndEps
    print(folderDest)
    # if season 2 continue, we do it a different way depending on the episode, 7 and 9 are weird so is 15
    # 16, the bottom like 5 lines, and 24
    if seas == "2":
        if epsNum not in ("01", "02", "03", "05", "07", "08", "09", "10", "11", "15", "16", "24"):
            print(quoteList[1].text.count("\n"))
            lines = quoteList[1].text.split("\n")
            lines = [quote for quote in lines if len(quote) != 0]
            linesCombined = ""
            linesCombined = concatQuotes(linesCombined, lines, folderDest)
            with open(folderDest, mode='a', encoding='utf-8') as f:
                f.write(linesCombined)
            # switch tabs
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
        if epsNum in ("07", "09", "15", "16", "24"):  # These episodes have to be extracted by all p elements
            linesCombined = ""
            for i in range(1, len(quoteList)):  # for all p elements
                lines = quoteList[i].text.split("\n")   # split lines by newlines
                lines = [quote for quote in lines if len(quote) != 0]  # list of lines that are not empty or newlines
                linesCombined = concatQuotes(linesCombined, lines, folderDest)
            # write to specified file
            with open(folderDest, mode='a', encoding='utf-8') as f:
                f.write(linesCombined)
            # switch tabs
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
    fileText = ""
    for i in range(1, len(quoteList)):
        try:
            if quoteList[i].text[0] in "([{<":  # if the quote is just a setting describer, or a note ignore it
                continue
        except IndexError: # most of the time is because of the gif at the bottom of the webpage, just continue
            print("error occurred in folderDest: " + folderDest + "\nProbably just a gif at the end")
            with open(folderDest, mode='a', encoding='utf-8') as f:
                f.write(fileText)
                continue
        if ":" in quoteList[i].text: # if the line isn't a quote, most of this is like END or CREDITS
            fileText = fileText + quoteList[i].text + "\n"
    with open(folderDest, mode='a', encoding='utf-8') as f:
        f.write(fileText)
    browser.close()
    browser.switch_to.window(browser.window_handles[0]) # Switch back to original tab
