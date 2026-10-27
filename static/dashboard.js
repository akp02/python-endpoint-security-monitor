
    const searchInput = document.getElementById("processSearch");
    const processTable = document.getElementById("processTable");
    const processCount = document.getElementById("processCount");

    const rows = Array.from(processTable.querySelectorAll("tr")).slice(1);
    const totalProcesses = rows.length;

    function filterProcesses() {
        const searchText = searchInput.value.toLowerCase().trim();
        let visibleProcesses = 0;

        rows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();
            const matches = rowText.includes(searchText);

            row.style.display = matches ? "" : "none";

            if (matches) {
                visibleProcesses++;
            }
        });

        processCount.textContent =
            `${visibleProcesses} of ${totalProcesses} processes shown`;
    }


const savedSearch = sessionStorage.getItem("processSearch");

if (savedSearch !== null) {
    searchInput.value = savedSearch;
}

searchInput.addEventListener("input", function () {
    sessionStorage.setItem("processSearch", searchInput.value);
    filterProcesses();
});

filterProcesses();


async function updateHealthMetrics() {
    try {
        const response = await fetch("/api/health");

        if (!response.ok) {
            throw new Error("Failed to retrieve CPU data");
        }

        const data = await response.json();

        document.getElementById("cpuUsage").textContent =
            data.cpu.cpu_usage_percent.toFixed(1) + "%";
        document.getElementById("ramUsage").textContent =
            data.memory.ram_usage_percent.toFixed(1) + "%";
        document.getElementById("diskUsage").textContent =
            data.disk.disk_percent.toFixed(1) + "%";


    } catch (error) {
        console.error("CPU update failed:", error);
    }
}

setInterval(updateHealthMetrics, 5000);



