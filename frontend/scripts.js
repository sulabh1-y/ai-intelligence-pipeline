async function loadPapers() {
    const container = document.getElementById("papers-container");
    container.innerHTML = "Loading...";

    try {
        const response = await fetch("https://ai-intelligence-pipeline.onrender.com/papers");
        const data = await response.json();

        container.innerHTML = "";

        data.forEach(paper => {
            const div = document.createElement("div");
            div.className = "card";

            div.innerHTML = `
                <h3>${paper.content.title}</h3>
                <p><b>Authors:</b> ${paper.content.authors.join(", ")}</p>
                <p><b>Category:</b> ${paper.content.category}</p>
                <p>${paper.content.summary}</p>
                <a href="${paper.content.link}" target="_blank">Read More</a>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        container.innerHTML = "Error loading papers 😢";
        console.error(error);
    }
}