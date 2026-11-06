(function () {
    if (window.__ELAINA_POST_LOCK_INITIALIZED__) {
        window.initEncryptedPostCast();
        return;
    }
    window.__ELAINA_POST_LOCK_INITIALIZED__ = true;

    const expectedDigest = "3fa5179a0d266b35635ae87d1b9ea61d8543e75605871069d924f9c515dc24aa";
    const storagePrefix = "elainaPostUnlock:v1:" + expectedDigest.slice(0, 12) + ":";

    function storageKey(box) {
        return storagePrefix + (box.dataset.pageKey || window.location.pathname);
    }

    function isRemembered(box) {
        try {
            return sessionStorage.getItem(storageKey(box)) === "1";
        } catch (_) {
            return false;
        }
    }

    function remember(box, unlocked) {
        try {
            if (unlocked) sessionStorage.setItem(storageKey(box), "1");
            else sessionStorage.removeItem(storageKey(box));
        } catch (_) {
            // Reading still works when browser storage is unavailable.
        }
    }

    function revealContent(box, focusContent) {
        const content = document.getElementById("post-content");
        if (!content) return;
        box.dataset.lockState = "open";
        box.hidden = true;
        box.style.display = "none";
        content.style.display = "block";
        content.classList.add("post-content--unlocked");
        const unlocked = document.getElementById("encrypt-unlocked");
        if (unlocked) unlocked.hidden = false;
        if (focusContent) {
            content.tabIndex = -1;
            content.focus({ preventScroll: true });
            content.scrollIntoView({ block: "start", behavior: "auto" });
        }
    }

    window.initEncryptedPostCast = function () {
        const box = document.getElementById("encrypt-box");
        if (!box) return;

        if (box.dataset.castReady !== "true") {
            const characters = window.__ELAINA_ENCRYPT_CHARACTERS__ || [];
            const image = box.querySelector("[data-encrypt-character]");
            if (characters.length && image) {
                const character = characters[Math.floor(Math.random() * characters.length)];
                box.dataset.encryptCharacter = character.id;
                box.style.setProperty("--encrypt-accent", character.accent);
                box.style.setProperty("--encrypt-accent-rgb", character.rgb);
                const name = box.querySelector("[data-encrypt-name]");
                const line = box.querySelector("[data-encrypt-line]");
                if (name) name.textContent = character.name;
                if (line) line.textContent = character.line;
                image.src = character.image;
                box.dataset.castReady = "true";
            }
        }

        if (isRemembered(box)) revealContent(box, false);
    };

    async function derivePostPassword(password) {
        const encoder = new TextEncoder();
        const key = await crypto.subtle.importKey(
            "raw",
            encoder.encode(password),
            "PBKDF2",
            false,
            ["deriveBits"]
        );
        const buffer = await crypto.subtle.deriveBits(
            {
                name: "PBKDF2",
                salt: encoder.encode("elainafan-post-lock-v2"),
                iterations: 180000,
                hash: "SHA-256"
            },
            key,
            256
        );
        return Array.from(new Uint8Array(buffer))
            .map(byte => byte.toString(16).padStart(2, "0"))
            .join("");
    }

    window.togglePostPassword = function () {
        const input = document.getElementById("pwd");
        const button = document.querySelector(".encrypt-box__reveal");
        if (!input || !button || input.readOnly) return;
        const visible = input.type === "password";
        input.type = visible ? "text" : "password";
        button.textContent = visible ? "隐藏" : "显示";
        button.setAttribute("aria-pressed", String(visible));
    };

    window.unlockEncryptedPost = async function () {
        const box = document.getElementById("encrypt-box");
        const input = document.getElementById("pwd");
        const message = document.getElementById("encrypt-message");
        if (!box || !input || box.dataset.lockState === "checking" || box.dataset.lockState === "open") return;

        if (!input.value) {
            input.setAttribute("aria-invalid", "true");
            if (message) message.textContent = "先输入暗号。";
            input.focus({ preventScroll: true });
            return;
        }
        if (!window.crypto || !window.crypto.subtle) {
            if (message) message.textContent = "当前浏览器无法验证暗号，请换一个浏览器再试。";
            return;
        }

        const button = box.querySelector(".encrypt-box__submit");
        const reveal = box.querySelector(".encrypt-box__reveal");
        const form = box.querySelector("form");
        box.dataset.lockState = "checking";
        input.removeAttribute("aria-invalid");
        input.readOnly = true;
        if (form) form.setAttribute("aria-busy", "true");
        if (button) {
            button.disabled = true;
            button.textContent = "确认中…";
        }
        if (reveal) reveal.disabled = true;
        if (message) message.textContent = "正在确认暗号…";

        try {
            const digest = await derivePostPassword(input.value);
            // A PJAX navigation may have replaced this page while the KDF ran.
            if (!box.isConnected || document.getElementById("encrypt-box") !== box) return;
            if (digest === expectedDigest) {
                const checkbox = document.getElementById("encrypt-remember");
                remember(box, !!checkbox && checkbox.checked);
                input.value = "";
                if (message) message.textContent = "";
                revealContent(box, true);
            } else {
                box.dataset.lockState = "idle";
                input.setAttribute("aria-invalid", "true");
                if (message) message.textContent = "暗号不对，再试一次。";
                input.focus({ preventScroll: true });
                input.select();
            }
        } catch (_) {
            if (box.isConnected) {
                box.dataset.lockState = "idle";
                if (message) message.textContent = "暂时无法验证，请再试一次。";
            }
        } finally {
            input.readOnly = false;
            if (form) form.removeAttribute("aria-busy");
            if (button) {
                button.disabled = false;
                button.textContent = "打开笔记";
            }
            if (reveal) reveal.disabled = false;
        }
    };

    window.lockEncryptedPost = function () {
        const box = document.getElementById("encrypt-box");
        const content = document.getElementById("post-content");
        if (!box || !content) return;
        remember(box, false);
        box.hidden = false;
        box.style.display = "";
        box.dataset.lockState = "idle";
        content.style.display = "none";
        content.classList.remove("post-content--unlocked");
        const unlocked = document.getElementById("encrypt-unlocked");
        if (unlocked) unlocked.hidden = true;
        const message = document.getElementById("encrypt-message");
        if (message) message.textContent = "";
        const input = document.getElementById("pwd");
        if (input) {
            input.type = "password";
            input.value = "";
            input.removeAttribute("aria-invalid");
            input.focus({ preventScroll: true });
        }
        const reveal = box.querySelector(".encrypt-box__reveal");
        if (reveal) {
            reveal.textContent = "显示";
            reveal.setAttribute("aria-pressed", "false");
        }
        box.scrollIntoView({ block: "center", behavior: "auto" });
    };

    document.addEventListener("input", event => {
        if (event.target.id !== "pwd") return;
        event.target.removeAttribute("aria-invalid");
        const box = document.getElementById("encrypt-box");
        const message = document.getElementById("encrypt-message");
        if (box && box.dataset.lockState === "idle" && message) message.textContent = "";
    });
    document.addEventListener("pjax:complete", window.initEncryptedPostCast);
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", window.initEncryptedPostCast, { once: true });
    } else {
        window.initEncryptedPostCast();
    }
})();
