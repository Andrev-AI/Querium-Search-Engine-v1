# Querium 

Portuguese and English version

## O que é?:
Querium é um Search Engine básico feito em Python, Querium usa tecnologias mais modernas para crawling, indexing, Pagerank e retorno de pesquisas. Querium foi projetado para que seu `Crawler` acesse páginas webs, busque por mais links e extraia/indexe o texto das páginas WEB. Após isso o `Indexer` receber o texto das páginas web e links e cria um index invertido, aplica **TF-IDF** para calcular a importância de cada termo no Index. Por fim o `Pagerank` que usa tanto **TF-IDF** e **BM25** para calcular cada termo com base na **query** de pesquisa. É um sistema básico que poderá ter evoluções no futuro e que possa ser integrado com IAs e até servir de auxílio para LLMs.

## Crawler

* Usa o `requests` para acessar as páginas e links das páginas. Começa por um array de links iniciais `start_urls` e começa achar mais links e ir seguindo e indexando conteúdos. Tem uma lista para evitar links repetidos.
* Caso o site dê `403` ou **badway request**. Usa `fake_useragent` e `proxies` para ultrapassar esse barramento.
* Usa sistema de depths que são links dentro de links, são links encontrado dentro de outras páginas criando uma árvore de links. Limitador `max_depth` controla o tamanho dessa árvore. Controlador `max_pages`  controla o link total de links de crawling.

## Indexer

* Cria um `json` salvando que é o index invertido con links e conteúdo extraído das páginas.
* Cria um index criando um importância de termos com TF-IDF.

## Pagerank

* `query` é onde se coloca a pesquisa, string palavra ou frase (em qualquer idioma). Com base nisso o **TF-IDF**, **BM25** e **Apontamento de página** para buscar no Index a palavra ou frases que melhor correspondem com a `query` e fazer ranqueamento de páginas. Esse sistema ainda é razoável e não busca muito bem e tem pontuações de páginas desrreguladas para buscar melhores correspondências.
* Ajustável os controladores do BM25 e TF-IDF para melhor ranqueamento.
* Ajustável pontuação para `url`, `body` (corpo do site) e `title`.

## Limitações

Sistema foi apenas um hobby de desenvolvimento baseado em minha fascinação por Search Engines e suas tecnologias. Por isso não é algo avançado mas em um futuro pode ser. Pode se aplicar IAs como **BERT** para tokenizar o Index e a query para melhor relacionar query com Index, outros algoritmos de verificação e pontuação de conteúdos. 
Outra importância é que os "regras/fatores de indexação ou ranqueamento", que em Search Engines profissionais são regras que os sites devem ter para obter melhores pontuações no ranquing, que geralmente são segredos bem guardados e protegidos, conténdo milhares de regras, esses sistema não apresenta mas já tenho ideias de como implementar no futuro.


# English:

## What is it?:
Querium is a basic Search Engine made in Python. Querium uses modern technologies for crawling, indexing, PageRank, and returning searches. Querium was designed for its `Crawler` to access web pages, search for more links, and extract/index the text from web pages. After that, the `Indexer` receives the text from the web pages and links and creates an inverted index, applying **TF-IDF** to calculate the importance of each term in the index. Finally, the `PageRank` uses both **TF-IDF** and **BM25** to calculate each term based on the search **query**. It is a basic system that can evolve in the future and be integrated with AIs, and even assist LLMs.

## Crawler

* Uses `requests` to access pages and links from the pages. It starts with an array of initial links `start_urls` and begins finding more links, following and indexing contents. It has a list to avoid duplicate links.
* If the site returns a `403` or **bad request**, it uses `fake_useragent` and `proxies` to bypass this barrier.
* Uses a depth system, which are links within links found on other pages, creating a link tree. The `max_depth` limiter controls the size of this tree. The `max_pages` controller controls the total number of links for crawling.

## Indexer

* Creates a `json` file saving the inverted index with links and extracted content from the pages.
* Creates an index calculating the importance of terms with TF-IDF.

## PageRank

* `query` is where you input the search, a string, word, or phrase (in any language). Based on this, **TF-IDF**, **BM25**, and **Page pointing** search the index for the word or phrases that best match the `query` and rank the pages. This system is still basic and does not search very well, with unregulated page scores for better matches.
* Adjustable controllers for BM25 and TF-IDF for better ranking.
* Adjustable scoring for `url`, `body` (page content), and `title`.

## Limitations

This system was just a hobby project based on my fascination with Search Engines and their technologies. Therefore, it is not advanced but may be in the future. AIs like **BERT** can be applied to tokenize the index and the query to better relate the query with the index, and other algorithms for content verification and scoring can be implemented.
Another important aspect is the "indexing or ranking rules/factors", which in professional Search Engines are rules that sites must follow to obtain better rankings. These are usually well-kept secrets containing thousands of rules, which this system does not present but I already have ideas on how to implement in the future.
