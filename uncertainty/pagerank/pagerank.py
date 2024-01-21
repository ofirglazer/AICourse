import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_model = dict()

    for iPage in corpus:
        trans_model[iPage] = (1 - damping_factor) / len(corpus)
    if len(corpus[page]):
        for next_page in corpus[page]:
            trans_model[next_page] += damping_factor / len(corpus[page])
    else:
        for next_page in trans_model:
            trans_model[next_page] += damping_factor / len(corpus)

    return trans_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    for page in corpus:
        page_rank[page] = 0

    page = random.choices(list(corpus.keys()))[0]
    page_rank[page] += 1

    for _ in range(n - 1):
        trans_model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(corpus.keys()), list(trans_model.values()))[0]
        page_rank[page] += 1

    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    eps = 0.001
    page_rank = dict()
    change = dict()
    for page in corpus:
        page_rank[page] = 1 / len(corpus)
        change[page] = 1
        if not len(corpus[page]):
            new_value = set()
            for p in corpus:
                new_value.add(p)
            corpus[page] = new_value

    while max(list(change.values())) > eps:
        for page in page_rank:
            old_pr = page_rank[page]
            page_rank[page] = 0

            for prev_page in corpus:
                if page in corpus[prev_page]:
                    page_rank[page] += page_rank[prev_page] / len(corpus[prev_page])
            page_rank[page] *= damping_factor

            page_rank[page] += (1 - damping_factor) / len(corpus)
            change[page] = abs(page_rank[page] - old_pr)
        pass

    return page_rank



if __name__ == "__main__":
    main()
