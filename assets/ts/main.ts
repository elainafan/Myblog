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

interface BangumiSearchSubject {
    id?: number;
    name: string;
    name_cn?: string;
    date?: string;
    rank?: number;
    rating?: {
        score?: number;
    };
    images?: {
        grid?: string;
        common?: string;
        medium?: string;
        large?: string;
    };
    fallbackUrl?: string;
}

interface BangumiSearchResponse {
    data?: BangumiSearchSubject[];
}

const BANGUMI_FALLBACK_SUBJECTS: BangumiSearchSubject[] = [
    { name: '千と千尋の神隠し', name_cn: '千与千寻', date: '2001', rating: { score: 8.6 }, rank: 25 },
    { name: 'カウボーイビバップ', name_cn: '星际牛仔', date: '1998', rating: { score: 8.8 }, rank: 18 },
    { name: '鋼の錬金術師 FULLMETAL ALCHEMIST', name_cn: '钢之炼金术师 FULLMETAL ALCHEMIST', date: '2009', rating: { score: 8.7 }, rank: 30 },
    { name: 'CLANNAD ～AFTER STORY～', name_cn: 'CLANNAD ～AFTER STORY～', date: '2008', rating: { score: 8.6 }, rank: 28 },
    { name: '攻殻機動隊 STAND ALONE COMPLEX', name_cn: '攻壳机动队 STAND ALONE COMPLEX', date: '2002', rating: { score: 8.5 }, rank: 55 },
    { name: '四月は君の嘘', name_cn: '四月是你的谎言', date: '2014', rating: { score: 7.9 }, rank: 320 },
    { name: '宇宙よりも遠い場所', name_cn: '比宇宙更远的地方', date: '2018', rating: { score: 8.2 }, rank: 140 },
    { name: '響け！ユーフォニアム', name_cn: '吹响！悠风号', date: '2015', rating: { score: 8.0 }, rank: 240 },
    { name: '少女終末旅行', name_cn: '少女终末旅行', date: '2017', rating: { score: 8.1 }, rank: 180 },
    { name: '蟲師', name_cn: '虫师', date: '2005', rating: { score: 8.5 }, rank: 45 }
];

const BANGUMI_RANDOM_TIMEOUT = 1600;
let bangumiRandomPool: BangumiSearchSubject[] = [];
let bangumiRandomRequest: Promise<BangumiSearchSubject[]> | null = null;

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
        const randomButton = root.querySelector('[data-bangumi-random]') as HTMLButtonElement;
        const randomResult = root.querySelector('[data-bangumi-random-result]') as HTMLAnchorElement;
        const randomCover = root.querySelector('[data-bangumi-random-cover]') as HTMLElement;
        const randomLabel = root.querySelector('[data-bangumi-random-label]') as HTMLElement;
        const randomTitle = root.querySelector('[data-bangumi-random-title]') as HTMLElement;
        const randomMeta = root.querySelector('[data-bangumi-random-meta]') as HTMLElement;
        const modal = root.querySelector('[data-bangumi-modal]') as HTMLElement;
        const modalCard = root.querySelector('[data-bangumi-modal-card]') as HTMLElement;
        const modalClose = root.querySelector('[data-bangumi-modal-close]') as HTMLButtonElement;
        const modalCover = root.querySelector('[data-bangumi-modal-cover]') as HTMLElement;
        const modalTitle = root.querySelector('[data-bangumi-modal-title]') as HTMLElement;
        const modalMeta = root.querySelector('[data-bangumi-modal-meta]') as HTMLElement;
        const modalComment = root.querySelector('[data-bangumi-modal-comment]') as HTMLElement;
        const modalLink = root.querySelector('[data-bangumi-modal-link]') as HTMLAnchorElement;
        if (!tabs.length || !panels.length) return;

        const activatePanel = (name: string) => {
            tabs.forEach(tab => {
                tab.setAttribute('aria-selected', String(tab.dataset.bangumiTab === name));
            });

            panels.forEach(panel => {
                panel.hidden = panel.dataset.bangumiPanel !== name;
            });
        };

        const renderPanel = (panel: HTMLElement) => {
            const grid = panel.querySelector('[data-bangumi-grid]') as HTMLElement;
            if (!grid) return;

            const cards = Array.from(grid.querySelectorAll('[data-bangumi-card]')) as HTMLElement[];
            const initial = Number(panel.dataset.bangumiInitial || 0);
            const mode = panel.dataset.bangumiView || 'rating';
            const limit = Number(panel.dataset.bangumiVisibleCount || (initial > 0 ? initial : cards.length));
            const sortedCards = sortBangumiCards(cards, mode);

            grid.querySelectorAll('.bangumi-year-divider').forEach(divider => divider.remove());

            let currentYear = '';
            sortedCards.forEach((card, index) => {
                const visible = index < limit || initial === 0;
                card.classList.toggle('is-hidden', !visible);

                if (mode === 'year' && visible) {
                    const year = card.dataset.bangumiYear || '未知年份';
                    if (year !== currentYear) {
                        const divider = document.createElement('div');
                        divider.className = 'bangumi-year-divider';
                        divider.textContent = year;
                        grid.appendChild(divider);
                        currentYear = year;
                    }
                }

                grid.appendChild(card);
            });

            const button = panel.querySelector('[data-bangumi-load]') as HTMLButtonElement;
            if (button) button.hidden = initial === 0 || limit >= sortedCards.length;
        };

        panels.forEach(panel => {
            panel.dataset.bangumiVisibleCount = panel.dataset.bangumiInitial && Number(panel.dataset.bangumiInitial) > 0
                ? panel.dataset.bangumiInitial
                : String(panel.querySelectorAll('[data-bangumi-card]').length);
            if (!panel.dataset.bangumiView) panel.dataset.bangumiView = 'rating';

            const button = panel.querySelector('[data-bangumi-load]') as HTMLButtonElement;
            renderPanel(panel);
            if (!button) return;

            button.addEventListener('click', () => {
                const step = Number(panel.dataset.bangumiStep || 8);
                const current = Number(panel.dataset.bangumiVisibleCount || 0);

                panel.dataset.bangumiVisibleCount = String(current + step);
                renderPanel(panel);
            });

            const viewButtons = panel.querySelectorAll('[data-bangumi-view]') as NodeListOf<HTMLButtonElement>;
            viewButtons.forEach(viewButton => {
                viewButton.addEventListener('click', () => {
                    const mode = viewButton.dataset.bangumiView || 'rating';
                    panel.dataset.bangumiView = mode;
                    panel.dataset.bangumiVisibleCount = panel.dataset.bangumiInitial && Number(panel.dataset.bangumiInitial) > 0
                        ? panel.dataset.bangumiInitial
                        : String(panel.querySelectorAll('[data-bangumi-card]').length);
                    viewButtons.forEach(button => {
                        button.setAttribute('aria-pressed', String(button.dataset.bangumiView === mode));
                    });
                    renderPanel(panel);
                });
            });
        });

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const name = tab.dataset.bangumiTab;
                if (name) activatePanel(name);
            });
        });

        if (randomButton && randomResult && randomCover && randomLabel && randomTitle && randomMeta) {
            queueBangumiRandomPrefetch();
            randomButton.addEventListener('click', () => {
                pickBangumiSubject(randomButton, randomResult, randomCover, randomLabel, randomTitle, randomMeta);
            });
        }

        if (modal && modalCard && modalClose && modalCover && modalTitle && modalMeta && modalComment && modalLink) {
            root.querySelectorAll('[data-bangumi-card]').forEach(card => {
                card.addEventListener('click', event => {
                    const mouseEvent = event as MouseEvent;
                    if (mouseEvent.ctrlKey || mouseEvent.metaKey || mouseEvent.shiftKey || mouseEvent.button !== 0) return;

                    event.preventDefault();
                    openBangumiModal(card as HTMLAnchorElement, modal, modalCover, modalTitle, modalMeta, modalComment, modalLink);
                });
            });

            modalClose.addEventListener('click', () => closeBangumiModal(modal));
            modal.addEventListener('click', event => {
                if (event.target === modal) closeBangumiModal(modal);
            });
        }

        const activeTab = Array.from(tabs).find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0];
        if (activeTab.dataset.bangumiTab) activatePanel(activeTab.dataset.bangumiTab);
    });
}

function sortBangumiCards(cards: HTMLElement[], mode: string) {
    return [...cards].sort((left, right) => {
        if (mode === 'year') {
            const yearDiff = Number(right.dataset.bangumiYear || 0) - Number(left.dataset.bangumiYear || 0);
            if (yearDiff) return yearDiff;
        }

        const rateDiff = Number(right.dataset.bangumiRate || 0) - Number(left.dataset.bangumiRate || 0);
        if (rateDiff) return rateDiff;

        const scoreDiff = Number(right.dataset.bangumiSiteScore || 0) - Number(left.dataset.bangumiSiteScore || 0);
        if (scoreDiff) return scoreDiff;

        return (left.dataset.bangumiTitle || '').localeCompare(right.dataset.bangumiTitle || '', 'zh-Hans');
    });
}

function openBangumiModal(card: HTMLAnchorElement, modal: HTMLElement, cover: HTMLElement, title: HTMLElement, meta: HTMLElement, comment: HTMLElement, link: HTMLAnchorElement) {
    const subjectTitle = card.dataset.bangumiTitle || card.textContent?.trim() || 'Untitled';
    const image = card.dataset.bangumiCover || '';
    const metaItems = [
        card.dataset.bangumiYear,
        card.dataset.bangumiRate && card.dataset.bangumiRate !== '0' ? `我的评分 ${card.dataset.bangumiRate}` : '',
        card.dataset.bangumiSiteScore && card.dataset.bangumiSiteScore !== '0' ? `Bangumi ${card.dataset.bangumiSiteScore}` : '',
        card.dataset.bangumiRank && card.dataset.bangumiRank !== '0' ? `#${card.dataset.bangumiRank}` : '',
        card.dataset.bangumiProgress
    ].filter(Boolean);

    cover.innerHTML = image ? `<img src="${image}" alt="${escapeHTML(subjectTitle)}" loading="lazy" referrerpolicy="no-referrer">` : '';
    title.textContent = subjectTitle;
    meta.textContent = metaItems.join(' · ');
    comment.textContent = card.dataset.bangumiComment || '暂无短评。';
    link.href = card.href;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
}

function closeBangumiModal(modal: HTMLElement) {
    modal.hidden = true;
    document.body.style.overflow = '';
}

async function pickBangumiSubject(button: HTMLButtonElement, result: HTMLAnchorElement, cover: HTMLElement, label: HTMLElement, title: HTMLElement, meta: HTMLElement) {
    button.disabled = true;
    button.textContent = bangumiRandomPool.length ? '抽取中...' : '连接 Bangumi...';

    try {
        if (!bangumiRandomPool.length) {
            bangumiRandomPool = await withTimeout(bangumiRandomRequest || fetchBangumiRandomCandidates(), BANGUMI_RANDOM_TIMEOUT);
        }
        if (!bangumiRandomPool.length) throw new Error('No Bangumi candidates');

        const index = Math.floor(Math.random() * bangumiRandomPool.length);
        const subject = bangumiRandomPool.splice(index, 1)[0];
        renderRandomBangumiSubject(subject, result, cover, label, title, meta, false);
        button.textContent = '再抽一部';
        if (bangumiRandomPool.length < 5) queueBangumiRandomPrefetch();
    } catch (err) {
        console.log('Failed to pick Bangumi subject', err);
        const subject = BANGUMI_FALLBACK_SUBJECTS[Math.floor(Math.random() * BANGUMI_FALLBACK_SUBJECTS.length)];
        renderRandomBangumiSubject(subject, result, cover, label, title, meta, true);
        button.textContent = '再抽一部';
    } finally {
        button.disabled = false;
    }
}

function queueBangumiRandomPrefetch() {
    if (bangumiRandomRequest || bangumiRandomPool.length >= 8) return;

    bangumiRandomRequest = fetchBangumiRandomCandidates()
        .then(candidates => {
            bangumiRandomPool = [...bangumiRandomPool, ...candidates].slice(-24);
            return candidates;
        })
        .catch(err => {
            console.log('Failed to prefetch Bangumi subjects', err);
            return [];
        })
        .finally(() => {
            bangumiRandomRequest = null;
        }) as Promise<BangumiSearchSubject[]>;
}

async function fetchBangumiRandomCandidates() {
    const offset = Math.floor(Math.random() * 1800);
    const response = await fetch(`https://api.bgm.tv/v0/subjects?type=2&sort=rank&limit=20&offset=${offset}`, {
        headers: {
            'Accept': 'application/json'
        }
    });

    if (!response.ok) throw new Error(`Bangumi request failed: ${response.status}`);

    const payload = await response.json() as BangumiSearchResponse;
    return (payload.data || []).filter(subject => {
        return subject.id && (subject.rating?.score || 0) >= 6;
    });
}

function withTimeout<T>(promise: Promise<T>, timeout: number) {
    return new Promise<T>((resolve, reject) => {
        const timer = window.setTimeout(() => reject(new Error('Bangumi request timeout')), timeout);

        promise
            .then(value => resolve(value))
            .catch(err => reject(err))
            .finally(() => window.clearTimeout(timer));
    });
}

function renderRandomBangumiSubject(subject: BangumiSearchSubject, result: HTMLAnchorElement, cover: HTMLElement, label: HTMLElement, title: HTMLElement, meta: HTMLElement, fallback: boolean) {
    const subjectTitle = subject.name_cn || subject.name || 'Untitled';
    const image = subject.images?.common || subject.images?.medium || subject.images?.large || subject.images?.grid;
    const year = subject.date ? subject.date.slice(0, 4) : '';
    const score = subject.rating?.score || 0;
    const metaItems = [
        year,
        score ? `Bangumi ${score}` : '',
        subject.rank ? `#${subject.rank}` : '',
        fallback ? '本地兜底' : ''
    ].filter(Boolean);

    result.href = subject.id
        ? `https://bangumi.tv/subject/${subject.id}`
        : `https://bangumi.tv/subject_search/${encodeURIComponent(subjectTitle)}?cat=2`;
    label.textContent = fallback ? 'Bangumi 随机推荐 · 兜底池' : 'Bangumi 随机推荐';
    title.textContent = subjectTitle;
    meta.textContent = metaItems.join(' · ');
    cover.innerHTML = image ? `<img src="${image}" alt="${escapeHTML(subjectTitle)}" loading="lazy" referrerpolicy="no-referrer">` : '';
    result.classList.add('is-visible');
}

function escapeHTML(value: string) {
    return value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
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

window.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('[data-bangumi-modal]').forEach(modal => {
        closeBangumiModal(modal as HTMLElement);
    });
});
