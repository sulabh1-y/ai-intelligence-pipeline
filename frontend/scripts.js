const API_URL = "https://ai-intelligence-pipeline.onrender.com";

async function getPapers() {
    const res = await fetch(`${API_URL}/papers`);
    const data = await res.json();

    let html = "";

    data.forEach(paper => {
        html += `
            <div style="margin-bottom:20px;">
                <h3>${paper.content.title}</h3>
                <p><b>Authors:</b> ${paper.content.authors.join(", ")}</p>
                <p>${paper.content.summary}</p>
                <hr/>
            </div>
        `;
    });

    document.getElementById("output").innerHTML = html;
}