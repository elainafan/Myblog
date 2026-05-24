/*!
*   Hugo Theme Stack
*
*   @author: Jimmy Cai
*   @website: https://jimmycai.com
*   @link: https://github.com/CaiJimmy/hugo-theme-stack
*/
import StackGallery from "ts/gallery";
// import { getColor } from 'ts/color'; 
import menu from 'ts/menu';
import createElement from 'ts/createElement';
import StackColorScheme from 'ts/colorScheme';
import { setupScrollspy } from 'ts/scrollspy';
import { setupSmoothAnchors } from "ts/smoothAnchors";
import { searchInit } from "ts/search";

const LONG_CODE_LINE_THRESHOLD = 80;

interface RandomPostItem {
    title: string;
    url: string;
}

function setupCodeBlocks() {
    const highlights = document.querySelectorAll('.article-content div.highlight') as NodeListOf<HTMLElement>;
    const copyText = `Copy`,
        copiedText = `Copied!`;

    highlights.forEach(highlight => {
        if (highlight.dataset.enhanced === 'true') return;
        highlight.dataset.enhanced = 'true';

        const codeBlock = highlight.querySelector('code[data-lang]') as HTMLElement;
        if (!codeBlock) return;

        const copyButton = document.createElement('button');
        copyButton.innerHTML = copyText;
        copyButton.classList.add('copyCodeButton');
        highlight.appendChild(copyButton);

        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(codeBlock.textContent)
                .then(() => {
                    copyButton.textContent = copiedText;

                    setTimeout(() => {
                        copyButton.textContent = copyText;
                    }, 1000);
                })
                .catch(err => {
                    alert(err)
                    console.log('Something went wrong', err);
                });
        });

        const lineCount = highlight.querySelectorAll('.lnt').length || (codeBlock.textContent || '').split('\n').length;
        if (lineCount <= LONG_CODE_LINE_THRESHOLD) return;

        highlight.classList.add('is-collapsible', 'is-collapsed');

        const expandButton = document.createElement('button');
        expandButton.type = 'button';
        expandButton.className = 'codeFoldButton';
        expandButton.textContent = `展开完整代码（${lineCount} 行）`;
        highlight.appendChild(expandButton);

        expandButton.addEventListener('click', () => {
            const collapsed = highlight.classList.toggle('is-collapsed');
            expandButton.textContent = collapsed ? `展开完整代码（${lineCount} 行）` : '收起代码';
        });
    });
}

function setupReadingProgress() {
    const existing = document.querySelector('.reading-progress') as HTMLElement;
    const article = document.querySelector('.article-page .main-article') as HTMLElement;
    const content = document.querySelector('.article-content') as HTMLElement;

    if (!article || !content) {
        existing?.remove();
        window.removeEventListener('scroll', updateReadingProgress);
        window.removeEventListener('resize', updateReadingProgress);
        return;
    }

    const bar = existing || document.createElement('div');
    bar.className = 'reading-progress';
    bar.setAttribute('aria-hidden', 'true');
    if (!existing) document.body.appendChild(bar);

    updateReadingProgress();
    window.removeEventListener('scroll', updateReadingProgress);
    window.removeEventListener('resize', updateReadingProgress);
    window.addEventListener('scroll', updateReadingProgress, { passive: true });
    window.addEventListener('resize', updateReadingProgress);
}

function updateReadingProgress() {
    const bar = document.querySelector('.reading-progress') as HTMLElement;
    const content = document.querySelector('.article-content') as HTMLElement;
    if (!bar || !content) return;

    const rect = content.getBoundingClientRect();
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const start = scrollTop + rect.top;
    const total = Math.max(content.scrollHeight - window.innerHeight * 0.55, 1);
    const current = Math.min(Math.max(scrollTop - start, 0), total);
    const progress = current / total;

    bar.style.transform = `scaleX(${progress})`;
}

function setupRandomWalk() {
    const links = document.querySelectorAll('[data-random-post]') as NodeListOf<HTMLAnchorElement>;
    const data = document.getElementById('random-posts-data');
    if (!links.length || !data?.textContent) return;

    let posts: RandomPostItem[];
    try {
        const parsed = JSON.parse(data.textContent);
        posts = typeof parsed === 'string' ? JSON.parse(parsed) : parsed;
    } catch (err) {
        console.log('Failed to parse random post list', err);
        return;
    }

    if (!Array.isArray(posts) || !posts.length) return;

    links.forEach(link => {
        if (link.dataset.randomBound === 'true') return;
        link.dataset.randomBound = 'true';

        link.addEventListener('click', event => {
            event.preventDefault();

            const currentPath = window.location.pathname.replace(/\/$/, '');
            const candidates = posts.filter(post => {
                const postPath = new URL(post.url, window.location.origin).pathname.replace(/\/$/, '');
                return postPath !== currentPath;
            });
            const pool = candidates.length ? candidates : posts;
            const post = pool[Math.floor(Math.random() * pool.length)];

            window.location.assign(post.url);
        });
    });
}

function setupBangumiCollection() {
    const roots = document.querySelectorAll('.bangumi-page') as NodeListOf<HTMLElement>;

    roots.forEach(root => {
        if (root.dataset.bangumiEnhanced === 'true') return;
        root.dataset.bangumiEnhanced = 'true';

        const tabs = root.querySelectorAll('[data-bangumi-tab]') as NodeListOf<HTMLButtonElement>;
        const panels = root.querySelectorAll('[data-bangumi-panel]') as NodeListOf<HTMLElement>;
        if (!tabs.length || !panels.length) return;

        const activatePanel = (name: string) => {
            tabs.forEach(tab => {
                tab.setAttribute('aria-selected', String(tab.dataset.bangumiTab === name));
            });

            panels.forEach(panel => {
                panel.hidden = panel.dataset.bangumiPanel !== name;
            });
        };

        panels.forEach(panel => {
            const button = panel.querySelector('[data-bangumi-load]') as HTMLButtonElement;
            if (!button) return;

            button.addEventListener('click', () => {
                const step = Number(panel.dataset.bangumiStep || 8);
                const hiddenCards = Array.from(panel.querySelectorAll('.bangumi-card.is-hidden')) as HTMLElement[];

                hiddenCards.slice(0, step).forEach(card => card.classList.remove('is-hidden'));
                if (!panel.querySelector('.bangumi-card.is-hidden')) button.hidden = true;
            });
        });

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const name = tab.dataset.bangumiTab;
                if (name) activatePanel(name);
            });
        });

        const activeTab = Array.from(tabs).find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0];
        if (activeTab.dataset.bangumiTab) activatePanel(activeTab.dataset.bangumiTab);
    });
}

let Stack = {
    init: () => {
        /**
         * Bind menu event
         */
        menu();

        const articleContent = document.querySelector('.article-content') as HTMLElement;
        if (articleContent) {
            new StackGallery(articleContent);
            setupSmoothAnchors();
            setupScrollspy();
        }

        // 调用search脚本初始化方法
        searchInit();
        setupReadingProgress();
        setupRandomWalk();
        setupBangumiCollection();

        /**
         * Add linear gradient background to tile style article
         */
        /** 
        const articleTile = document.querySelector('.article-list--tile');
        if (articleTile) {
            let observer = new IntersectionObserver(async (entries, observer) => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;
                    observer.unobserve(entry.target);

                    const articles = entry.target.querySelectorAll('article.has-image');
                    articles.forEach(async articles => {
                        const image = articles.querySelector('img'),
                            imageURL = image.src,
                            key = image.getAttribute('data-key'),
                            hash = image.getAttribute('data-hash'),
                            articleDetails: HTMLDivElement = articles.querySelector('.article-details');

                        const colors = await getColor(key, hash, imageURL);

                        articleDetails.style.background = `
                        linear-gradient(0deg, 
                            rgba(${colors.DarkMuted.rgb[0]}, ${colors.DarkMuted.rgb[1]}, ${colors.DarkMuted.rgb[2]}, 0.5) 0%, 
                            rgba(${colors.Vibrant.rgb[0]}, ${colors.Vibrant.rgb[1]}, ${colors.Vibrant.rgb[2]}, 0.75) 100%)`;
                    })
                })
            });

            observer.observe(articleTile)
        }
        */


        setupCodeBlocks();

        new StackColorScheme(document.getElementById('dark-mode-toggle'));
    }
}

window.addEventListener('load', () => {
    setTimeout(function () {
        Stack.init();
    }, 0);
})

declare global {
    interface Window {
        createElement: any;
        Stack: any
    }
}

window.Stack = Stack;
window.createElement = createElement;
