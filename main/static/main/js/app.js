document.addEventListener("DOMContentLoaded", function () {
    /* =========================================
       Плавное появление при скролле
       ========================================= */
    const elements = document.querySelectorAll(".fade-in");

    if (elements.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        }, {
            threshold: 0.15
        });

        elements.forEach((el) => observer.observe(el));
    }

    /* =========================================
       Выход из аккаунта
       ========================================= */
    document.addEventListener("click", function (e) {
        if (e.target.closest(".logout-link")) {
            e.preventDefault();

            const logoutForm = document.getElementById("logout-form");
            if (logoutForm) {
                logoutForm.submit();
            }
        }
    });

    /* =========================================
       Бургер-меню
       ========================================= */
    const burgerBtn = document.getElementById("burgerBtn");
    const mobilePanel = document.getElementById("mobilePanel");

    if (burgerBtn && mobilePanel) {
        burgerBtn.addEventListener("click", function () {
            document.body.classList.toggle("nav-open");
        });
    }

    /* =========================================
       3D-эффект карточек на главной
       ========================================= */
    const featureCards = document.querySelectorAll(".feature-card");

    featureCards.forEach((card) => {
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const rotateX = (y / rect.height - 0.5) * 8;
            const rotateY = (x / rect.width - 0.5) * -8;

            card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
        });

        card.addEventListener("mouseleave", () => {
            card.style.transform = "perspective(800px) rotateX(0) rotateY(0) translateY(0)";
        });
    });

    /* =========================================
       Анимация счётчиков
       Работает только для чисел типа 10+ / 100+
       Не трогает 24/7
       ========================================= */
    const statNumbers = document.querySelectorAll(".mini-stat-number");

    statNumbers.forEach((el) => {
        const text = el.innerText.trim();

        if (text.includes("/")) {
            return;
        }

        const hasPlus = text.includes("+");
        const target = parseInt(text.replace(/\D/g, ""), 10);

        if (isNaN(target)) {
            return;
        }

        let count = 0;
        el.innerText = "0" + (hasPlus ? "+" : "");

        const interval = setInterval(() => {
            count += Math.ceil(target / 30);

            if (count >= target) {
                count = target;
                clearInterval(interval);
            }

            el.innerText = count + (hasPlus ? "+" : "");
        }, 30);
    });

    /* =========================================
       Hover-эффект для кнопок
       ========================================= */
    const heroButtons = document.querySelectorAll(".hero-btn");

    heroButtons.forEach((btn) => {
        btn.addEventListener("mouseenter", () => {
            btn.style.transform = "translateY(-2px)";
        });

        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "translateY(0)";
        });
    });

    /* =========================================
       Красивая валидация теста
       ========================================= */
    const form = document.querySelector(".test-box");

    if (form) {
        const questionCards = form.querySelectorAll(".question-card");

        // Убираем ошибку сразу после выбора ответа
        questionCards.forEach((question) => {
            const inputs = question.querySelectorAll("input[type='radio']");

            inputs.forEach((input) => {
                input.addEventListener("change", function () {
                    question.classList.remove("error");
                });
            });
        });

        // Проверка при отправке
        form.addEventListener("submit", function (e) {
            let firstError = null;
            let hasError = false;

            questionCards.forEach((question) => {
                const checked = question.querySelector("input[type='radio']:checked");

                if (!checked) {
                    question.classList.add("error");

                    if (!firstError) {
                        firstError = question;
                    }

                    hasError = true;
                } else {
                    question.classList.remove("error");
                }
            });

            if (hasError) {
                e.preventDefault();

                if (firstError) {
                    firstError.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                }
            }
        });
    }
});