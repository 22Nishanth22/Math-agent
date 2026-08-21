topics = ["Linear algebra","Vector space","Matrix multiplication","Eigenvalues and eigenvectors","Singular value decomposition",
    "Principal component analysis","Multivariable calculus","Partial derivative","Gradient","Jacobian matrix",
    "Hessian matrix","Chain rule","Taylor series","Mathematical optimization","Convex optimization","Gradient descent",
    "Probability theory","Conditional probability","Bayes' theorem","Random variable","Probability distribution",
    "Normal distribution","Bernoulli distribution","Binomial distribution","Expected value","Variance",
    "Covariance","Correlation","Law of large numbers","Central limit theorem","Maximum likelihood estimation",
    "Bayesian inference","Statistical estimation","Statistical hypothesis testing","Confidence interval",
    "Regression analysis","Linear regression","Logistic regression","Regularization (mathematics)",
    "Entropy (information theory)","Cross-entropy","Kullback–Leibler divergence","Mutual information",
    "Information gain","Distance","Euclidean distance","Manhattan distance","Norm (mathematics)","Inner product space"
]


import json

import wikipedia as wk
wk.set_lang("en")
wk.wikipedia.USER_AGENT = "Project (YOUR-MAIL-ID)"




CUTOFF_MARKERS = ["== See also ==", "== References ==", "== Further reading ==",
                  "== External links ==","== Notes ==","== Citations =="]


def clean_wiki_content(content):
    earliest_cutoff = len(content)
    for marker in CUTOFF_MARKERS:
        idx = content.find(marker)
        if idx != -1:
            earliest_cutoff = min(earliest_cutoff, idx)
    return content[:earliest_cutoff].strip()



def pull_corpus(output_path: str):
    corpus = []

    for title in topics:
        full_page = wk.page(title, auto_suggest=False)
        corpus.append({
            "title": full_page.title,
            "pageid": full_page.pageid,
            "content": clean_wiki_content(full_page.content)
            })

    with open(f"agentic_rag/data/raw/{output_path}.json", "w", encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(corpus)} articles")
    return corpus