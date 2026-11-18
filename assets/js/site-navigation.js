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

    window.addEventListener("onColorSchemeChange", () => {
        const widget = document.querySelector("giscus-widget");
        if (widget) setCommentTheme(widget);
    });

    if (window.Pjax?.isSupported?.()) {
        window.pjax = new Pjax({
            elements: "a[href], form[action]:not([data-result-title])",
            selectors: [".main-container"],
            switches: { ".main-container": switchPage },
            cacheBust: false
        });
        document.addEventListener("pjax:send", () => window.topbar?.show());
        document.addEventListener("pjax:complete", () => window.topbar?.hide());
        document.addEventListener("pjax:success", () => {
            const url = new URL(location.href);
            url.searchParams.delete("t");
            if (url.hash.includes("?")) {
                const [anchor, query] = url.hash.split("?");
                const params = new URLSearchParams(query);
                params.delete("t");
                url.hash = anchor + (params.size ? "?" + params : "");
            }
            if (url.href !== location.href) {
                history.replaceState({ ...history.state, url: url.href }, "", url.href);
            }
            updatePage();
            window.Stack?.init();
        });
    }
    updatePage();
})();
