(function () {
    const pageMetadata = [
        'link[rel="canonical"]', 'link[rel="alternate"]', 'meta[name="description"]',
        'meta[name="keywords"]', 'meta[name="robots"]', 'meta[property^="og:"]',
        'meta[property^="article:"]', 'meta[name^="twitter:"]'
    ].join(",");

    function switchPage(oldMain, newMain, options) {
        const next = newMain.ownerDocument;
        document.title = options.title = next.title;
        document.body.className = next.body.className;
        document.documentElement.lang = next.documentElement.lang;
        document.documentElement.dir = next.documentElement.dir;
        document.head.querySelectorAll(pageMetadata).forEach(element => element.remove());
        next.head.querySelectorAll(pageMetadata).forEach(element => {
            document.head.appendChild(document.importNode(element, true));
        });
        window.Pjax.switches.outerHTML.call(this, oldMain, newMain, options);
    }

    function setCommentTheme(widget) {
        const dark = document.documentElement.dataset.scheme === "dark";
        widget.setAttribute("theme", dark ? widget.dataset.darkTheme : widget.dataset.lightTheme);
    }

    function mountComments() {
        const template = document.querySelector("template[data-giscus]");
        if (!template) return;

        // Instantiate only after PJAX has updated the URL and head. Each widget
        // owns its iframe and removes its message listener when disconnected.
        const widget = template.content.firstElementChild.cloneNode(true);
        setCommentTheme(widget);
        template.replaceWith(widget);
        if (!customElements.get("giscus-widget") && !document.getElementById("giscus-module")) {
            const script = document.createElement("script");
            script.id = "giscus-module";
            script.type = "module";
            script.src = "https://cdn.jsdelivr.net/npm/giscus@1.6.0/+esm";
            script.onerror = () => script.remove();
            document.head.appendChild(script);
        }
    }

    function renderMath() {
        const marker = document.querySelector(".math-katex");
        if (!marker) return;
        let attempts = 0;
        function render() {
            if (!marker.isConnected) return;
            if (typeof window.renderMathInElement !== "function" || !window.katex) {
                if (++attempts < 30) setTimeout(render, 500);
                return;
            }
            window.renderMathInElement(marker.closest(".main-article") || document.body, {
                delimiters: [
                    { left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false },
                    { left: "\\(", right: "\\)", display: false }, { left: "\\[", right: "\\]", display: true }
                ],
                ignoredClasses: ["gist", "katex"]
            });
        }
        render();
    }

    function updatePage() {
        mountComments();
        renderMath();
        const timer = document.getElementById("runningdays");
        if (timer) {
            const minutes = Math.floor((Date.now() - new Date(2025, 5, 23).getTime()) / 60000);
            timer.textContent = Math.floor(minutes / 1440) + "天" + Math.floor(minutes / 60) % 24 + "小时" + minutes % 60 + "分钟";
        }
        if (!document.body.classList.contains("article-page")) {
            document.querySelectorAll("#viewCount").forEach(element => { element.style.display = "none"; });
        }
        // Vercount reads the current URL and DOM once per script execution.
        document.getElementById("page-view-counter")?.remove();
        const counter = document.createElement("script");
        counter.id = "page-view-counter";
        counter.src = "https://cn.vercount.one/js";
        document.body.appendChild(counter);
    }

    function documentUrl(url) {
        return url.origin + url.pathname + url.search;
    }

    function fragmentTarget(hash) {
        if (!hash) return null;
        try {
            const id = decodeURIComponent(hash.slice(1));
            return document.getElementById(id) || document.getElementsByName(id)[0];
        } catch (_) {
            return null;
        }
    }

    function stopPendingNavigation(pjax) {
        pjax.abortRequest(pjax.request);
        window.topbar?.hide();
    }

    function bindAnchorNavigation(pjax) {
        document.addEventListener("click", event => {
            if (event.defaultPrevented || event.button !== 0 ||
                event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            const link = event.target.closest?.('a[href*="#"]');
            if (!link || link.hasAttribute("download") ||
                (link.target && link.target.toLowerCase() !== "_self")) return;

            let targetUrl;
            try {
                targetUrl = new URL(link.href);
            } catch (_) {
                return;
            }
            const current = new URL(location.href);
            if (documentUrl(targetUrl) !== documentUrl(current)) return;
            const target = fragmentTarget(targetUrl.hash);
            if (!target) return;

            event.preventDefault();
            stopPendingNavigation(pjax);
            const top = target.getBoundingClientRect().top + window.scrollY;
            if (targetUrl.href !== current.href) {
                // Fragment visits belong to this PJAX document and share its uid.
                const state = {
                    ...history.state,
                    uid: history.state?.uid ?? pjax.lastUid,
                    title: document.title,
                    url: current.href,
                    scrollPos: [window.scrollX, window.scrollY]
                };
                history.replaceState(state, "", current.href);
                history.pushState({ ...state, url: targetUrl.href, scrollPos: [window.scrollX, top] }, "", targetUrl.href);
            }
            const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
            window.scrollTo({ top, behavior: reduceMotion ? "instant" : "smooth" });
        });
    }

    window.addEventListener("onColorSchemeChange", () => {
        const widget = document.querySelector("giscus-widget");
        if (widget) setCommentTheme(widget);
    });

    if (window.Pjax?.isSupported?.()) {
        const pjax = window.pjax = new Pjax({
            elements: "a[href], form[action]:not([data-result-title])",
            selectors: [".main-container"],
            switches: { ".main-container": switchPage },
            cacheBust: false
        });
        let renderedUrl = documentUrl(new URL(location.href));
        const loadUrl = pjax.loadUrl.bind(pjax);
        pjax.loadUrl = (href, options) => {
            // PJAX 0.2.8 passes history:false for back/forward navigation.
            if (options?.history !== false) return loadUrl(href, options);

            const targetUrl = new URL(location.href);
            if (documentUrl(targetUrl) !== renderedUrl) return loadUrl(targetUrl.href, options);

            stopPendingNavigation(pjax);
            const target = fragmentTarget(targetUrl.hash);
            const position = options.scrollPos ||
                [0, target ? target.getBoundingClientRect().top + window.scrollY : 0];
            window.scrollTo({ left: position[0], top: position[1], behavior: "instant" });
        };
        bindAnchorNavigation(pjax);
        document.addEventListener("pjax:send", () => window.topbar?.show());
        document.addEventListener("pjax:complete", () => window.topbar?.hide());
        document.addEventListener("pjax:success", event => {
            const url = new URL(location.href);
            url.searchParams.delete("t");
            if (url.hash.includes("?")) {
                const [anchor, query] = url.hash.split("?");
                const params = new URLSearchParams(query);
                params.delete("t");
                url.hash = anchor + (params.size ? "?" + params : "");
            }
            // PJAX overwrites the destination entry before swapping on popstate.
            // Put its saved scroll position back so later fragment visits can use it.
            const scrollPos = event.history === false && event.scrollPos;
            if (url.href !== location.href || scrollPos) {
                const state = { ...history.state, url: url.href };
                if (scrollPos) state.scrollPos = scrollPos;
                history.replaceState(state, "", url.href);
            }
            renderedUrl = documentUrl(url);
            updatePage();
            window.Stack?.init();
        });
    }
    updatePage();
})();
