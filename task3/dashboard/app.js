document.addEventListener("DOMContentLoaded", () => {
    // 1. Initial configuration and setup
    let chartMonthly = null;
    let chartCategory = null;
    let chartSegments = null;

    // Dom elements
    const selectCity = document.getElementById("filter-city");
    const selectCategory = document.getElementById("filter-category");
    const selectSegment = document.getElementById("filter-segment");
    const selectGender = document.getElementById("filter-gender");
    const selectAgeGroup = document.getElementById("filter-age-group");
    const filterStatusEl = document.getElementById("filter-status");
    const btnReset = document.getElementById("btn-reset");

    // KPI Elements
    const kpiRevenue = document.getElementById("kpi-revenue");
    const kpiOrders = document.getElementById("kpi-orders");
    const kpiAov = document.getElementById("kpi-aov");
    const kpiCustomers = document.getElementById("kpi-customers");
    const kpiWeekend = document.getElementById("kpi-weekend");
    const topCustomersBody = document.getElementById("top-customers-body");

    // Currency Formatter (Indian Rupees)
    const formatCurrency = (val) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(val);
    };

    // 2. Initialize filter options dynamically from data
    const initFilters = () => {
        const cities = [...new Set(salesData.map(d => d.City))].sort();
        const categories = [...new Set(salesData.map(d => d.Category))].sort();
        const segments = [...new Set(salesData.map(d => d.RFM_Segment))].sort();

        cities.forEach(city => {
            const opt = document.createElement("option");
            opt.value = city;
            opt.textContent = city;
            selectCity.appendChild(opt);
        });

        categories.forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat;
            opt.textContent = cat;
            selectCategory.appendChild(opt);
        });

        segments.forEach(seg => {
            const opt = document.createElement("option");
            opt.value = seg;
            opt.textContent = seg;
            selectSegment.appendChild(opt);
        });
    };

    // 3. Filtering and aggregation logic
    const filterAndRender = () => {
        const cityVal = selectCity.value;
        const catVal = selectCategory.value;
        const segVal = selectSegment.value;
        const genVal = selectGender.value;
        const ageVal = selectAgeGroup.value;

        // Apply filters
        const filtered = salesData.filter(d => {
            return (cityVal === "All" || d.City === cityVal) &&
                   (catVal === "All" || d.Category === catVal) &&
                   (segVal === "All" || d.RFM_Segment === segVal) &&
                   (genVal === "All" || d.Gender === genVal) &&
                   (ageVal === "All" || d.Age_Group === ageVal);
        });

        // Update status text
        filterStatusEl.textContent = `Showing ${filtered.length.toLocaleString()} of ${salesData.length.toLocaleString()} transactions`;

        // Calculate KPIs
        const totalSales = filtered.reduce((sum, d) => sum + d.Total_Sales, 0);
        const totalOrders = filtered.length;
        const aov = totalOrders > 0 ? totalSales / totalOrders : 0;
        const uniqueCustomers = new Set(filtered.map(d => d.Customer_ID)).size;
        
        // Weekend share calculation
        // Filter by Is_Weekend (which is boolean in the dataset)
        const weekendSales = filtered.filter(d => d.Is_Weekend).reduce((sum, d) => sum + d.Total_Sales, 0);
        const weekendPct = totalSales > 0 ? (weekendSales / totalSales) * 100 : 0;

        // Render KPIs
        kpiRevenue.textContent = formatCurrency(totalSales);
        kpiOrders.textContent = totalOrders.toLocaleString();
        kpiAov.textContent = formatCurrency(aov);
        kpiCustomers.textContent = uniqueCustomers.toLocaleString();
        kpiWeekend.textContent = `${weekendPct.toFixed(1)}%`;

        // Render Charts & Tables
        renderMonthlyTrend(filtered);
        renderCategoryShare(filtered);
        renderRfmSegments(filtered);
        renderTopCustomers(filtered);
    };

    // 4. Charting functions
    // A. Line Chart: Monthly Revenue
    const renderMonthlyTrend = (data) => {
        // Group by month
        const monthlyData = {};
        data.forEach(d => {
            const month = d.Order_Date.substring(0, 7); // YYYY-MM
            monthlyData[month] = (monthlyData[month] || 0) + d.Total_Sales;
        });

        const months = Object.keys(monthlyData).sort();
        const revenues = months.map(m => monthlyData[m]);

        const ctx = document.getElementById("chart-monthly-trend").getContext("2d");
        
        if (chartMonthly) {
            chartMonthly.destroy();
        }

        chartMonthly = new Chart(ctx, {
            type: "line",
            data: {
                labels: months,
                datasets: [{
                    label: "Monthly Revenue (INR)",
                    data: revenues,
                    borderColor: "#818cf8",
                    backgroundColor: "rgba(129, 140, 248, 0.15)",
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: "#38bdf8",
                    pointBorderColor: "#ffffff",
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `Revenue: ${formatCurrency(context.parsed.y)}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: "rgba(255, 255, 255, 0.05)" },
                        ticks: { color: "#94a3b8" }
                    },
                    y: {
                        grid: { color: "rgba(255, 255, 255, 0.05)" },
                        ticks: {
                            color: "#94a3b8",
                            callback: (value) => `₹${(value / 1e5).toFixed(0)}L`
                        }
                    }
                }
            }
        });
    };

    // B. Donut Chart: Category Share
    const renderCategoryShare = (data) => {
        const catData = {};
        data.forEach(d => {
            catData[d.Category] = (catData[d.Category] || 0) + d.Total_Sales;
        });

        const categories = Object.keys(catData);
        const revenues = categories.map(c => catData[c]);
        
        const ctx = document.getElementById("chart-category-share").getContext("2d");
        
        if (chartCategory) {
            chartCategory.destroy();
        }

        chartCategory = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: categories,
                datasets: [{
                    data: revenues,
                    backgroundColor: ["#818cf8", "#38bdf8", "#34d399", "#f87171", "#fbbf24"],
                    borderWidth: 2,
                    borderColor: "#1e293b"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: "#cbd5e1", boxWidth: 12, padding: 15 }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
                                return `${context.label}: ${formatCurrency(context.raw)} (${pct}%)`;
                            }
                        }
                    }
                },
                cutout: "60%"
            }
        });
    };

    // C. Bar Chart: RFM Segments
    const renderRfmSegments = (data) => {
        // Group transactions by unique Customer_ID and get their segments
        const customerSegments = {};
        const seenCustomers = new Set();

        data.forEach(d => {
            if (!seenCustomers.has(d.Customer_ID)) {
                seenCustomers.add(d.Customer_ID);
                customerSegments[d.RFM_Segment] = (customerSegments[d.RFM_Segment] || 0) + 1;
            }
        });

        const segments = ["Champions", "Loyal Customers", "Average Spenders", "New Customers", "At Risk", "Lost / Low-Value"];
        const counts = segments.map(seg => customerSegments[seg] || 0);

        const ctx = document.getElementById("chart-rfm-segments").getContext("2d");
        
        if (chartSegments) {
            chartSegments.destroy();
        }

        chartSegments = new Chart(ctx, {
            type: "bar",
            data: {
                labels: segments.map(s => s.split(" ")[0]), // Use short names on x-axis labels
                datasets: [{
                    data: counts,
                    backgroundColor: ["#34d399", "#818cf8", "#fbbf24", "#38bdf8", "#f87171", "#64748b"],
                    borderWidth: 1,
                    borderColor: "rgba(255, 255, 255, 0.1)"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            title: (context) => segments[context[0].dataIndex],
                            label: (context) => `Customers: ${context.raw}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: "#94a3b8" }
                    },
                    y: {
                        grid: { color: "rgba(255, 255, 255, 0.05)" },
                        ticks: { color: "#94a3b8", precision: 0 }
                    }
                }
            }
        });
    };

    // D. Table: Render Top Customers
    const renderTopCustomers = (data) => {
        // Aggregate monetary and frequency by unique customer
        const customerMap = {};
        data.forEach(d => {
            if (!customerMap[d.Customer_ID]) {
                customerMap[d.Customer_ID] = {
                    Customer_ID: d.Customer_ID,
                    Customer_Name: d.Customer_Name,
                    City: d.City,
                    Orders: 0,
                    Total_Spend: 0,
                    RFM_Segment: d.RFM_Segment
                };
            }
            customerMap[d.Customer_ID].Orders += 1;
            customerMap[d.Customer_ID].Total_Spend += d.Total_Sales;
        });

        // Convert map to array, sort by Total_Spend descending, take top 10
        const sortedCustomers = Object.values(customerMap)
            .sort((a, b) => b.Total_Spend - a.Total_Spend)
            .slice(0, 10);

        // Clear existing table body
        topCustomersBody.innerHTML = "";

        if (sortedCustomers.length === 0) {
            const row = document.createElement("tr");
            row.innerHTML = `<td colspan="7" class="text-center py-4 text-slate-500">No customer records matching selected filters.</td>`;
            topCustomersBody.appendChild(row);
            return;
        }

        // Segment badges styling helper
        const getSegmentBadgeClass = (seg) => {
            switch(seg) {
                case "Champions": return "bg-emerald-500/10 border-emerald-500/30 text-emerald-400";
                case "Loyal Customers": return "bg-indigo-500/10 border-indigo-500/30 text-indigo-400";
                case "New Customers": return "bg-sky-500/10 border-sky-500/30 text-sky-400";
                case "Average Spenders": return "bg-amber-500/10 border-amber-500/30 text-amber-400";
                case "At Risk": return "bg-rose-500/10 border-rose-500/30 text-rose-400";
                default: return "bg-slate-500/10 border-slate-500/30 text-slate-400";
            }
        };

        sortedCustomers.forEach((cust, index) => {
            const row = document.createElement("tr");
            row.className = "hover:bg-slate-800/20 border-b border-slate-800/40 text-slate-300";
            row.innerHTML = `
                <td class="py-2.5 font-bold text-slate-400">${index + 1}</td>
                <td class="py-2.5 font-mono">${cust.Customer_ID}</td>
                <td class="py-2.5">${cust.Customer_Name}</td>
                <td class="py-2.5 text-slate-400">${cust.City}</td>
                <td class="py-2.5 text-center">${cust.Orders}</td>
                <td class="py-2.5 text-right">
                    <span class="border px-2 py-0.5 rounded-full text-[9px] font-bold ${getSegmentBadgeClass(cust.RFM_Segment)}">
                        ${cust.RFM_Segment}
                    </span>
                </td>
                <td class="py-2.5 text-right font-semibold text-indigo-300">${formatCurrency(cust.Total_Spend)}</td>
            `;
            topCustomersBody.appendChild(row);
        });
    };

    // 5. Setup event listeners
    const setupListeners = () => {
        selectCity.addEventListener("change", filterAndRender);
        selectCategory.addEventListener("change", filterAndRender);
        selectSegment.addEventListener("change", filterAndRender);
        selectGender.addEventListener("change", filterAndRender);
        selectAgeGroup.addEventListener("change", filterAndRender);

        btnReset.addEventListener("click", () => {
            selectCity.value = "All";
            selectCategory.value = "All";
            selectSegment.value = "All";
            selectGender.value = "All";
            selectAgeGroup.value = "All";
            filterAndRender();
        });
    };

    // 6. Run Initialization
    initFilters();
    setupListeners();
    filterAndRender(); // First draw
});
