document
.getElementById("capture-page")
.addEventListener("click", async function (e) {

    e.preventDefault();

    const originalScroll = window.scrollY;

    // Go to the top
    window.scrollTo(0, 0);

    // Wait for scrolling to finish
    await new Promise(resolve => setTimeout(resolve, 300));

    const page = document.documentElement;

    const canvas = await html2canvas(page, {

        useCORS: true,

        allowTaint: true,

        backgroundColor: null,

        scale: 2,

        scrollX: 0,

        scrollY: 0,

        width: page.scrollWidth,

        height: page.scrollHeight,

        windowWidth: page.scrollWidth,

        windowHeight: page.scrollHeight

    });

    // Restore scroll position
    window.scrollTo(0, originalScroll);

    const link = document.createElement("a");

    const filename = window.location.href
    .replace(/^https?:\/\//, "")
    .replace(/[\/:?&=#]+/g, "_");

    link.download = `${filename}.png`;

    link.href = canvas.toDataURL("image/png");

    link.click();

});