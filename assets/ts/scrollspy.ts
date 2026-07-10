// Implements a scroll spy system for the ToC, displaying the current section with an indicator and scrolling to it when needed.

// Inspired from https://gomakethings.com/debouncing-your-javascript-events/
function debounced(func: Function) {
    let timeout;
    return () => {
        if (timeout) {
            window.cancelAnimationFrame(timeout);
        }

        timeout = window.requestAnimationFrame(() => func());
    }
}

const headersQuery = ".article-content h1[id], .article-content h2[id], .article-content h3[id], .article-content h4[id], .article-content h5[id], .article-content h6[id]";
const tocQuery = "#TableOfContents";
const navigationQuery = "#TableOfContents li";
const activeClass = "active-class";

let cleanupScrollspy: (() => void) | undefined;

function scrollToTocElement(tocElement: HTMLElement, scrollableNavigation: HTMLElement) {
    const navigationRect = scrollableNavigation.getBoundingClientRect();
    const elementRect = tocElement.getBoundingClientRect();
    const scrollTop = scrollableNavigation.scrollTop
        + elementRect.top
        - navigationRect.top
        - (navigationRect.height - elementRect.height) / 2;

    scrollableNavigation.scrollTo({ top: Math.max(0, scrollTop), behavior: "smooth" });
}

type IdToElementMap = { [key: string]: HTMLElement };

function buildIdToNavigationElementMap(navigation: NodeListOf<Element>): IdToElementMap {
    const sectionLinkRef: IdToElementMap = {};
    navigation.forEach((navigationElement: HTMLElement) => {
        const link = navigationElement.querySelector("a");
        const href = link.getAttribute("href");
        if (href.startsWith("#")) {
            sectionLinkRef[href.slice(1)] = navigationElement;
        }
    });

    return sectionLinkRef;
}

function computeOffsets(headers: NodeListOf<Element>) {
    let sectionsOffsets = [];
    const documentScrollTop = window.scrollY || document.documentElement.scrollTop;

    headers.forEach((header: HTMLElement) => {
        sectionsOffsets.push({
            id: header.id,
            offset: header.getBoundingClientRect().top + documentScrollTop
        });
    });
    sectionsOffsets.sort((a, b) => a.offset - b.offset);
    return sectionsOffsets;
}

function setupScrollspy() {
    cleanupScrollspy?.();
    cleanupScrollspy = undefined;

    let headers = document.querySelectorAll(headersQuery);
    if (headers.length === 0) {
        console.warn("No header matched query", headers);
        return;
    }

    let scrollableNavigation = document.querySelector(tocQuery) as HTMLElement | undefined;
    if (!scrollableNavigation) {
        console.warn("No toc matched query", tocQuery);
        return;
    }

    let navigation = document.querySelectorAll(navigationQuery);
    if (navigation.length === 0) {
        console.warn("No navigation matched query", navigationQuery);
        return;
    }

    let sectionsOffsets = computeOffsets(headers);

    // We need to avoid scrolling when the user is actively interacting with the ToC. Otherwise, if the user clicks on a link in the ToC,
    // we would scroll their view, which is not optimal usability-wise.
    let tocHovered: boolean = false;
    const mouseenterHandler = debounced(() => tocHovered = true);
    const mouseleaveHandler = debounced(() => tocHovered = false);
    scrollableNavigation.addEventListener("mouseenter", mouseenterHandler);
    scrollableNavigation.addEventListener("mouseleave", mouseleaveHandler);

    let activeSectionLink: Element;

    let idToNavigationElement: IdToElementMap = buildIdToNavigationElementMap(navigation);

    function scrollHandler() {
        let scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;

        let newActiveSection: HTMLElement | undefined;
        const activationOffset = Math.min(window.innerHeight * 0.25, 240);

        // Find the section that is currently active.
        // It is possible for no section to be active, so newActiveSection may be undefined.
        sectionsOffsets.forEach((section) => {
            if (scrollPosition >= section.offset - activationOffset) {
                newActiveSection = document.getElementById(section.id);
            }
        });

        // Find the link for the active section. Once again, there are a few edge cases:
        // - No active section = no link => undefined
        // - No active section but the link does not exist in toc (e.g. because it is outside of the applicable ToC levels) => undefined
        let newActiveSectionLink: HTMLElement | undefined
        if (newActiveSection) {
            newActiveSectionLink = idToNavigationElement[newActiveSection.id];
        }

        if (newActiveSection && !newActiveSectionLink) {
            // The active section does not have a link in the ToC, so we can't scroll to it.
            console.debug("No link found for section", newActiveSection);
        } else if (newActiveSectionLink !== activeSectionLink) {
            if (activeSectionLink)
                activeSectionLink.classList.remove(activeClass);
            if (newActiveSectionLink) {
                newActiveSectionLink.classList.add(activeClass);
                if (!tocHovered) {
                    // Scroll so that newActiveSectionLink is in the middle of scrollableNavigation, except when it's from a manual click (hence the tocHovered check)
                    scrollToTocElement(newActiveSectionLink, scrollableNavigation);
                }
            }
            activeSectionLink = newActiveSectionLink;
        }
    }

    const windowScrollHandler = debounced(scrollHandler);
    window.addEventListener("scroll", windowScrollHandler, { passive: true });
    
    // Resizing may cause the offset values to change: recompute them.
    function resizeHandler() {
        sectionsOffsets = computeOffsets(headers);
        scrollHandler();
    }

    const windowResizeHandler = debounced(resizeHandler);
    window.addEventListener("resize", windowResizeHandler);

    const articleContent = document.querySelector(".article-content");
    const contentResizeObserver = articleContent && typeof ResizeObserver !== "undefined"
        ? new ResizeObserver(debounced(resizeHandler))
        : undefined;
    contentResizeObserver?.observe(articleContent);

    cleanupScrollspy = () => {
        window.removeEventListener("scroll", windowScrollHandler);
        window.removeEventListener("resize", windowResizeHandler);
        scrollableNavigation.removeEventListener("mouseenter", mouseenterHandler);
        scrollableNavigation.removeEventListener("mouseleave", mouseleaveHandler);
        contentResizeObserver?.disconnect();
    };

    scrollHandler();
}

export { setupScrollspy };
