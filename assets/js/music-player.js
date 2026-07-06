(function () {
    const STORAGE_KEY = "elainaMusicPlayerState";
    const PLAYER_ID = "elaina-music-player";
    const ALGORITHM_ENTRY_TRACK_NAMES = ["Magia", "Everyday World"];
    const PLAYBACK_MODES = ["list", "random", "repeat-one"];
    const PLAYBACK_MODE_LABELS = {
        list: "List loop",
        random: "Shuffle",
        "repeat-one": "Repeat one"
    };

    const icons = {
        prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6h2v12H6z"/><path d="m18 6-8 6 8 6z"/></svg>',
        play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m8 5 11 7-11 7z"/></svg>',
        pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7z"/><path d="M13 5h4v14h-4z"/></svg>',
        next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 6h2v12h-2z"/><path d="m6 6 8 6-8 6z"/></svg>',
        list: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7h11v2H8z"/><path d="M8 11h11v2H8z"/><path d="M8 15h11v2H8z"/><path d="M4 7h2v2H4z"/><path d="M4 11h2v2H4z"/><path d="M4 15h2v2H4z"/></svg>',
        modeList: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7h10v2H5z"/><path d="M5 11h10v2H5z"/><path d="M5 15h10v2H5z"/><path d="m17 8 3 3-3 3z"/></svg>',
        modeRandom: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 4h4v4h-2V7.4l-3.7 3.7-1.4-1.4L17.6 6H17z"/><path d="M3 7h3.2c1.6 0 2.7.6 3.7 1.9l4.2 5.2c.7.9 1.3 1.2 2.4 1.2H17v-1.6l4 3.3-4 3.3V18h-.5c-1.8 0-3-.6-4.2-2.1L8.1 10.7C7.4 9.8 6.9 9.5 6 9.5H3z"/><path d="M3 16.5h3c.9 0 1.4-.3 2.1-1.2l1-1.2 1.5 1.9-.7.9C8.8 19.1 7.7 19 6 19H3z"/></svg>',
        modeRepeatOne: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7h8.5c2.5 0 4.5 2 4.5 4.5S18 16 15.5 16H14v-2h1.5c1.4 0 2.5-1.1 2.5-2.5S16.9 9 15.5 9H7.8l2.1 2.1-1.4 1.4L4 8l4.5-4.5 1.4 1.4z"/><path d="M17 17H8.5C6 17 4 15 4 12.5S6 8 8.5 8H10v2H8.5C7.1 10 6 11.1 6 12.5S7.1 15 8.5 15h7.7l-2.1-2.1 1.4-1.4L20 16l-4.5 4.5-1.4-1.4z"/><path d="M11 10h2v6h-2z"/></svg>'
    };

    function normalizeSong(song) {
        return {
            name: song && song.name ? String(song.name) : "Unknown",
            artist: song && song.artist ? String(song.artist) : "",
            url: song && song.url ? String(song.url) : "",
            cover: song && song.cover ? String(song.cover) : "",
            sourceUrl: song && song.sourceUrl ? String(song.sourceUrl) : ""
        };
    }

    function getPlaylist() {
        const rawPlaylist = Array.isArray(window.__ELAINA_MUSIC_PLAYLIST__)
            ? window.__ELAINA_MUSIC_PLAYLIST__
            : [];

        return rawPlaylist
            .map(normalizeSong)
            .filter(song => song.url);
    }

    function clampNumber(value, min, max) {
        const number = Number(value);
        if (!Number.isFinite(number)) return min;
        return Math.min(Math.max(number, min), max);
    }

    function readState() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
        } catch (error) {
            return {};
        }
    }

    function createIconButton(action, label, icon) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "music-player__icon-button";
        button.dataset.action = action;
        button.title = label;
        button.setAttribute("aria-label", label);
        button.innerHTML = icon;
        return button;
    }

    function setImageSource(image, url) {
        image.hidden = !url;
        image.src = url || "";
        image.onerror = () => {
            image.hidden = true;
        };
    }

    function createMusicPlayer(initialPlaylist) {
        let playlist = initialPlaylist;
        let savedState = readState();
        let currentIndex = clampNumber(savedState.index, 0, Math.max(playlist.length - 1, 0));
        let pendingSeek = clampNumber(savedState.currentTime, 0, Number.MAX_SAFE_INTEGER);
        let lastEntryMusicKey = null;
        let progressFrame = 0;
        let isExpanded = savedState.expanded === true;
        let playbackMode = PLAYBACK_MODES.includes(savedState.mode) ? savedState.mode : "list";

        const audio = new Audio();
        audio.preload = "metadata";
        audio.volume = clampNumber(savedState.volume ?? 0.82, 0, 1);

        const root = document.createElement("section");
        root.id = PLAYER_ID;
        root.className = "music-player";
        root.setAttribute("aria-label", "Music player");
        if (isExpanded) root.classList.add("music-player--expanded");

        const panel = document.createElement("div");
        panel.className = "music-player__panel";
        panel.setAttribute("aria-hidden", String(!isExpanded));

        const panelHead = document.createElement("div");
        panelHead.className = "music-player__panel-head";

        const panelCoverWrap = document.createElement("div");
        panelCoverWrap.className = "music-player__panel-cover";
        const panelCover = document.createElement("img");
        panelCover.alt = "";
        panelCover.loading = "lazy";
        panelCoverWrap.append(panelCover);

        const panelMeta = document.createElement("div");
        panelMeta.className = "music-player__panel-meta";
        const panelTitle = document.createElement("div");
        panelTitle.className = "music-player__panel-title";
        const panelArtist = document.createElement("div");
        panelArtist.className = "music-player__panel-artist";
        panelMeta.append(panelTitle, panelArtist);
        panelHead.append(panelCoverWrap, panelMeta);

        const list = document.createElement("div");
        list.className = "music-player__list";
        list.setAttribute("role", "listbox");
        panel.append(panelHead, list);

        const dock = document.createElement("div");
        dock.className = "music-player__dock";

        const coverButton = document.createElement("button");
        coverButton.type = "button";
        coverButton.className = "music-player__cover-button";
        coverButton.title = "Playlist";
        coverButton.setAttribute("aria-label", "Playlist");
        const cover = document.createElement("img");
        cover.alt = "";
        cover.loading = "lazy";
        coverButton.append(cover);

        const info = document.createElement("div");
        info.className = "music-player__info";
        const title = document.createElement("div");
        title.className = "music-player__title";
        const artist = document.createElement("div");
        artist.className = "music-player__artist";
        const progress = document.createElement("input");
        progress.className = "music-player__progress";
        progress.type = "range";
        progress.min = "0";
        progress.max = "1000";
        progress.value = "0";
        progress.step = "1";
        progress.title = "Seek";
        progress.setAttribute("aria-label", "Seek");
        info.append(title, artist, progress);

        const controls = document.createElement("div");
        controls.className = "music-player__controls";
        const prevButton = createIconButton("prev", "Previous", icons.prev);
        const playButton = createIconButton("play", "Play", icons.play);
        playButton.classList.add("music-player__icon-button--primary");
        const nextButton = createIconButton("next", "Next", icons.next);
        const modeButton = createIconButton("mode", PLAYBACK_MODE_LABELS[playbackMode], icons.modeList);
        const listButton = createIconButton("list", "Playlist", icons.list);
        controls.append(prevButton, playButton, nextButton, modeButton, listButton);

        dock.append(coverButton, info, controls);
        root.append(panel, dock);
        document.body.append(root);

        function saveState() {
            const state = {
                index: currentIndex,
                currentTime: Number.isFinite(audio.currentTime) ? audio.currentTime : 0,
                paused: audio.paused,
                volume: audio.volume,
                expanded: isExpanded,
                mode: playbackMode
            };
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        }

        function currentSong() {
            return playlist[currentIndex] || playlist[0];
        }

        function isAlgorithmEntryTrack(index) {
            const song = playlist[index];
            return !!song && ALGORITHM_ENTRY_TRACK_NAMES.includes(song.name);
        }

        function setExpanded(nextExpanded) {
            isExpanded = nextExpanded;
            root.classList.toggle("music-player--expanded", isExpanded);
            panel.setAttribute("aria-hidden", String(!isExpanded));
            saveState();
        }

        function updateProgress() {
            progressFrame = 0;
            const duration = Number.isFinite(audio.duration) && audio.duration > 0 ? audio.duration : 0;
            const ratio = duration > 0 ? clampNumber(audio.currentTime / duration, 0, 1) : 0;
            const progressValue = Math.round(ratio * 1000);
            progress.value = String(progressValue);
            progress.style.setProperty("--music-progress", `${ratio * 100}%`);
            saveState();
        }

        function requestProgressUpdate() {
            if (progressFrame) return;
            progressFrame = window.requestAnimationFrame(updateProgress);
        }

        function updatePlayButton() {
            const isPlaying = !audio.paused;
            root.classList.toggle("music-player--playing", isPlaying);
            playButton.title = isPlaying ? "Pause" : "Play";
            playButton.setAttribute("aria-label", isPlaying ? "Pause" : "Play");
            playButton.innerHTML = isPlaying ? icons.pause : icons.play;
        }

        function updateModeButton() {
            const iconKey = {
                list: "modeList",
                random: "modeRandom",
                "repeat-one": "modeRepeatOne"
            }[playbackMode];
            const label = PLAYBACK_MODE_LABELS[playbackMode];

            modeButton.dataset.mode = playbackMode;
            modeButton.title = label;
            modeButton.setAttribute("aria-label", label);
            modeButton.innerHTML = icons[iconKey];
        }

        function cyclePlaybackMode() {
            const currentModeIndex = PLAYBACK_MODES.indexOf(playbackMode);
            playbackMode = PLAYBACK_MODES[(currentModeIndex + 1) % PLAYBACK_MODES.length];
            updateModeButton();
            saveState();
        }

        function renderSong() {
            const song = currentSong();
            if (!song) return;

            title.textContent = song.name;
            artist.textContent = song.artist;
            panelTitle.textContent = song.name;
            panelArtist.textContent = song.artist;
            setImageSource(cover, song.cover);
            setImageSource(panelCover, song.cover);

            list.querySelectorAll(".music-player__track").forEach((button, index) => {
                const isCurrent = index === currentIndex;
                button.classList.toggle("music-player__track--current", isCurrent);
                button.setAttribute("aria-selected", String(isCurrent));
            });
        }

        function renderList() {
            const fragment = document.createDocumentFragment();
            playlist.forEach((song, index) => {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "music-player__track";
                button.dataset.index = String(index);
                button.setAttribute("role", "option");

                const trackCover = document.createElement("span");
                trackCover.className = "music-player__track-cover";
                if (song.cover) {
                    const image = document.createElement("img");
                    image.src = song.cover;
                    image.alt = "";
                    image.loading = "lazy";
                    image.onerror = () => image.remove();
                    trackCover.append(image);
                }

                const trackText = document.createElement("span");
                trackText.className = "music-player__track-text";
                const trackTitle = document.createElement("span");
                trackTitle.className = "music-player__track-title";
                trackTitle.textContent = song.name;
                const trackArtist = document.createElement("span");
                trackArtist.className = "music-player__track-artist";
                trackArtist.textContent = song.artist;
                trackText.append(trackTitle, trackArtist);

                button.append(trackCover, trackText);
                fragment.append(button);
            });
            list.replaceChildren(fragment);
            renderSong();
        }

        function playSafely() {
            const result = audio.play();
            if (result && typeof result.catch === "function") {
                result.catch(() => {
                    updatePlayButton();
                    saveState();
                });
            }
        }

        function switchTrack(index, options) {
            const normalizedIndex = clampNumber(index, 0, playlist.length - 1);
            const song = playlist[normalizedIndex];
            if (!song) return;

            currentIndex = normalizedIndex;
            pendingSeek = clampNumber(options && options.seek, 0, Number.MAX_SAFE_INTEGER);
            audio.src = song.url;
            audio.load();
            renderSong();
            updateProgress();

            if (options && options.autoplay) {
                playSafely();
            }
            saveState();
        }

        function randomIndex(excludingIndex) {
            if (playlist.length <= 1) return 0;
            let nextIndex = excludingIndex;
            while (nextIndex === excludingIndex) {
                nextIndex = Math.floor(Math.random() * playlist.length);
            }
            return nextIndex;
        }

        function nextTrack(options) {
            if (playlist.length === 0) return;

            if (playbackMode === "repeat-one" && !(options && options.manual)) {
                switchTrack(currentIndex, { autoplay: true });
                return;
            }

            const nextIndex = playbackMode === "random"
                ? randomIndex(currentIndex)
                : (currentIndex + 1) % playlist.length;
            switchTrack(nextIndex, { autoplay: true });
        }

        function previousTrack() {
            const nextIndex = currentIndex <= 0 ? playlist.length - 1 : currentIndex - 1;
            switchTrack(nextIndex, { autoplay: true });
        }

        function playArticleEntryMusic() {
            const article = document.querySelector(".main-article[data-entry-music='algorithm-random']");
            if (!article) {
                lastEntryMusicKey = null;
                return;
            }

            if (isAlgorithmEntryTrack(currentIndex)) {
                return;
            }

            const algorithmTrackIndexes = playlist
                .map((song, index) => ALGORITHM_ENTRY_TRACK_NAMES.includes(song.name) ? index : -1)
                .filter(index => index >= 0);
            if (algorithmTrackIndexes.length === 0) {
                return;
            }

            const pageKey = article.dataset.pageKey || window.location.pathname;
            if (lastEntryMusicKey === pageKey) {
                return;
            }
            lastEntryMusicKey = pageKey;

            const candidateIndex = algorithmTrackIndexes[Math.floor(Math.random() * algorithmTrackIndexes.length)];
            switchTrack(candidateIndex, { autoplay: true });
        }

        function setPlaylist(nextPlaylist) {
            if (!Array.isArray(nextPlaylist) || nextPlaylist.length === 0) return;
            playlist = nextPlaylist;
            currentIndex = clampNumber(currentIndex, 0, playlist.length - 1);
            renderList();
        }

        audio.addEventListener("loadedmetadata", () => {
            if (pendingSeek > 0 && Number.isFinite(audio.duration)) {
                audio.currentTime = Math.min(pendingSeek, Math.max(audio.duration - 0.25, 0));
            }
            pendingSeek = 0;
            updateProgress();
        });
        audio.addEventListener("play", () => {
            updatePlayButton();
            saveState();
        });
        audio.addEventListener("pause", () => {
            updatePlayButton();
            saveState();
        });
        audio.addEventListener("timeupdate", requestProgressUpdate);
        audio.addEventListener("ended", nextTrack);
        audio.addEventListener("volumechange", saveState);

        progress.addEventListener("input", () => {
            if (!Number.isFinite(audio.duration) || audio.duration <= 0) return;
            const ratio = clampNumber(Number(progress.value) / 1000, 0, 1);
            audio.currentTime = audio.duration * ratio;
            updateProgress();
        });

        controls.addEventListener("click", event => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;

            switch (button.dataset.action) {
                case "prev":
                    previousTrack();
                    break;
                case "play":
                    if (audio.paused) {
                        playSafely();
                    } else {
                        audio.pause();
                    }
                    break;
                case "next":
                    nextTrack({ manual: true });
                    break;
                case "mode":
                    cyclePlaybackMode();
                    break;
                case "list":
                    setExpanded(!isExpanded);
                    break;
            }
        });

        coverButton.addEventListener("click", () => setExpanded(!isExpanded));
        list.addEventListener("click", event => {
            const button = event.target.closest(".music-player__track");
            if (!button) return;
            switchTrack(Number(button.dataset.index), { autoplay: true });
        });
        document.addEventListener("keydown", event => {
            if (event.key === "Escape" && isExpanded) {
                setExpanded(false);
            }
        });
        window.addEventListener("beforeunload", saveState);

        renderList();
        switchTrack(currentIndex, { seek: pendingSeek, autoplay: savedState.paused === false });
        updatePlayButton();
        updateModeButton();

        return {
            setPlaylist,
            syncPage: playArticleEntryMusic
        };
    }

    function initMusicPlayer() {
        const playlist = getPlaylist();
        if (playlist.length === 0) {
            window.playArticleEntryMusic = function () {};
            return;
        }

        if (window.ElainaMusicPlayer) {
            window.ElainaMusicPlayer.setPlaylist(playlist);
            window.ElainaMusicPlayer.syncPage();
            return;
        }

        if (document.getElementById(PLAYER_ID)) return;
        window.ElainaMusicPlayer = createMusicPlayer(playlist);
        window.playArticleEntryMusic = function () {
            if (window.ElainaMusicPlayer) {
                window.ElainaMusicPlayer.syncPage();
            }
        };
        window.ElainaMusicPlayer.syncPage();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initMusicPlayer, { once: true });
    } else {
        initMusicPlayer();
    }
    document.addEventListener("pjax:complete", initMusicPlayer);
})();
