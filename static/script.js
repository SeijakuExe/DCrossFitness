document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("notificationToggle");
    const dropdown = document.getElementById("notificationDropdown");
    const list = document.getElementById("notificationList");
    const badge = document.querySelector(".notification-badge strong");

    let loaded = false;

    toggle.addEventListener("click", function (e) {
        e.preventDefault();
        dropdown.classList.toggle("show");

        if (dropdown.classList.contains("show") && !loaded) {
            fetch('/api/notifications')
                .then(res => res.json())
                .then(data => {
                    list.innerHTML = '';
                    if (data.length === 0) {
                        list.innerHTML = '<li class="notification-empty">No notifications</li>';
                    } else {
                        data.forEach(noti => {
                            const li = document.createElement('li');
                            li.className = 'notification-item' + (noti.Status === 'Uncheck' ? ' unread' : '');
                            li.innerHTML = `
                                <div class="notification-content">
                                    <span class="notification-desc">${noti.Description}</span><br/>
                                    <small class="notification-time">${new Date(noti.Time).toLocaleString()}</small>
                                </div>
                            `;
                            list.appendChild(li);
                        });
                    }
                    loaded = true;

                    // Đánh dấu đã đọc và ẩn badge
                    fetch('/api/notifications/mark-read', { method: 'POST' })
                        .then(() => {
                            if (badge) {
                                badge.style.display = 'none'; // ẩn badge sau khi đánh dấu đã đọc
                            }
                        });
                })
                .catch(error => {
                    console.error('Lỗi khi fetch notifications:', error);
                });
        }
    });

    document.addEventListener("click", function (e) {
        if (!toggle.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove("show");
            loaded = false;
        }
    });
});



document.addEventListener("DOMContentLoaded", function () {
    const body = document.querySelector("body"),
        sidebar = document.querySelector(".sidebar"),
        toggle = document.querySelector(".toggle"),
        modeSwitch = document.querySelector(".toggle-switch"),
        modeText = document.querySelector(".mode-text"),
        homeSection = document.querySelector(".home");

    const storedTheme = localStorage.getItem("theme");
    if (storedTheme === "dark") {
        body.classList.add("dark");
        modeText.innerText = "Light Mode";
    }

    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");
        modeText.innerText = body.classList.contains("dark") ? "Light Mode" : "Dark Mode";
        if (body.classList.contains("dark")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.removeItem("theme");
        }
    });;

    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });



    function loadMembershipContent() {
        homeSection.innerHTML = `
            <div class="title">Membership</div>
            <div class="membership-container">
                <div class="membership-box">
                    <h2>Standard Membership</h2>
                    <ul class="benefits-list">
                        <li>Access to the gym 5 days/week</li>
                        <li>Basic guidance from a trainer</li>
                        <li>Use of treadmills and cycling machines</li>
                        <li>Free sauna access</li>
                        <li>10% discount on other services</li>
                    </ul>
                    <a href="/select-plan?plan=Basic">
                        <button type="button">Select Plan</button>
                    </a>
                </div>
                <div class="membership-box">
                    <h2>Premium Membership</h2>
                    <ul class="benefits-list">
                        <li>Unlimited gym access</li>
                        <li>One-on-one personal training</li>
                        <li>Full access to all gym equipment</li>
                        <li>Free drinks & locker service</li>
                        <li>20% discount on other services</li>
                    </ul>
                    <a href="/select-plan?plan=Premium">
                        <button type="button">Select Plan</button>
                    </a>
                </div>
            </div>
        `;
    }

    function loadUserProfile() {
    fetch('/profile')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const account = data.account;

                fetch('/profile')
                    .then(res => res.json())
                    .then(membershipData => {
                        let membershipHTML = `
                            <div class="title">My Memberships</div>
                            <div class="user-info">
                                <table class="membership-table">
                                    <thead>
                                        <tr>
                                            <th>Type</th>
                                            <th>Start Date</th>
                                            <th>End Date</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                        `;

                        let activeMembership = null;

                        if (membershipData.status === "success") {
                            membershipData.memberships.forEach(membership => {
                                if (membership.ID === membershipData.in_use) {
                                    activeMembership = membership;
                                }

                                membershipHTML += `
                                    <tr>
                                        <td>${membership["Membership Type"]}</td>
                                        <td>${membership["Start Date"]}</td>
                                        <td>${membership["End Date"] || "N/A"}</td>
                                        <td>${membership.Status}</td>
                                    </tr>
                                `;
                            });
                        } else {
                            membershipHTML += "<tr><td colspan='4'>No memberships found.</td></tr>";
                        }

                        membershipHTML += `</tbody></table>`;

                        membershipHTML += activeMembership
                            ? `
                                <div class="membership-status">
                                <div class="current-membership">
                                    <h3>Currently in use:</h3>
                                    <p><strong>Type:</strong> ${activeMembership["Membership Type"]}</p>
                                    <p><strong>Start Date:</strong> ${activeMembership["Start Date"]}</p>
                                    <p><strong>End Date:</strong> ${activeMembership["End Date"] || "N/A"}</p>

                                </div>
                                <div class="days-left"><div>${membershipData.days_left} days left</div></div>
                                </div>
                              `
                            : `<p><strong>Current Membership:</strong> None</p>`;

                        membershipHTML += `</div>`;

                        homeSection.innerHTML = `
                            <div class="title">User</div>
                            <div class="user-info">
                                <p><strong>Name:</strong> ${account.Name}</p>
                                <p><strong>ID:</strong> ${account.ID}</p>
                                <p><strong>Phone:</strong> ${account.Phone}</p>
                                <p><strong>Username:</strong> ${account.Username}</p>
                                <p><strong>Gender:</strong> ${account.Gender}</p>
                                <p><strong>Birth:</strong> ${account.Birth || "N/A"}</p>
                                <div class="btn-container-wide">
                                    <a href="/edit-profile" class="btn-wide btn-submit">Edit profile</a>
                                    <a href="/change-password" class="btn-wide btn-submit">Change password</a>
                                </div>
                            </div>
                            <div class="membership-info">
                                ${membershipHTML}
                            </div><br><br>
                        `;
                    })
                    .catch(err => {
                        console.error("Error loading memberships:", err);
                        homeSection.innerHTML += "<p>Error loading memberships.</p>";
                    });

            } else {
                homeSection.innerHTML = `<div class="text">Error</div><p>${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
            homeSection.innerHTML = `<div class="text">Error</div><p>Failed to load user data.</p>`;
        });
}


    function loadDashboardContent() {
        homeSection.innerHTML = `
            <div class="title">Dashboard</div>
            <div class="intro-container body-container">
                <h1>Welcome to <br>D-Cross Fitness</h1>
                <p>Locally gym and calisthenic facilities service.</p>
            </div>
            <div class="body-container">
                <div class="block-container">

                    <a href="https://maps.app.goo.gl/yBvj3MjzqGiNefHs7" target="_blank">
                        <div class="block block-1">
                            <h2 class="text"><i class='bx bxs-map'></i> ADDRESS:</h2>
                            <div class="text"><br>P. Hoa Ma, Ngo Thi Nham,<br> Hai Ba Trung, Ha Noi, Vietnam.</div>
                        </div>
                    </a>

                    <a href="https://www.timeanddate.com/worldclock/vietnam/hanoi" target="_blank">
                        <div class="block block-2">
                            <h2 class="text"><i class='bx bx-time'></i> OPENING HOURS:</h2>
                            <div class="text">MON - FRI: &nbsp;&nbsp;9 AM - 6 PM</div>
                            <div class="text">SATURDAY: &nbsp;&nbsp;8 AM - 8 PM</div>
                            <div class="text">SUNDAY: &nbsp;&nbsp;1 PM - 8 PM</div>
                        </div>
                    </a>

                    <a href="#" class="block block-3 nav-link" data-content="Membership">
                        <h2 class="text"><i class='bx bxs-credit-card'></i> PURCHASE PLANS:</h2>
                        <div class="text">Outstanding services access <br>from less than 10$/month.</div>
                        <div class="text">Advance course with personal trainers.</div>
                        <div class="text">Online payment available.</div>
                    </a>

                    <a href="facilities">
                        <div class="block block-4">
                            <h2><i class='bx bx-archive'></i> FACILITIES:</h2>
                            <div class="text"><br>General standard and <br>universal choice.</div>
                            <div class="text">Accessible archive</div>
                        </div>
                    </a>

                    <a href="collection">
                        <div class="block block-5">
                            <h2 class="text"><i class='bx bxs-hot'></i> WORKOUT COLLECTION:</h2>
                            <div class="text">Study some workouts by yourself!</div>
                        </div>
                    </a>

                    <a href="#">
                        <div class="block block-6">
                            <h2 class="text"><i class='bx bxs-contact'></i> CONTACT US:</h2>
                            <div class="text"><br>Via phone, email, etc.</div>
                        </div>
                    </a>
                </div>
            </div>
            <div class="intro-container body-container">
                <h2>Transform Your Fitness Today</h2>
                <p><br>Unleash your potential with our unique gym and calisthenics fusion. Build strength, boost endurance, and master flexibility. Our expert trainers and top-notch facilities guarantee results. <br><br>Join now and get a free professional training session—limited spots available! Don’t miss out.</p>
            </div>
            <div class="body-container">
                <div class="block block-bottom">
                    <i class='bx bxs-to-top'></i>
                    <div><br>BACK TO TOP</div>
                </div>
            </div>
        `;

        document.querySelector(".block-bottom").addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }



function loadTransactionsContent() {
    fetch('/profile')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                let transactionHTML = `
                    <div class="title">Transactions</div>
                    <div class="transaction-two-columns">
                        <div class="transaction-column">
                            <h3>Sent Transactions</h3>
                `;

                if (data.transactions.length > 0) {
                    data.transactions.forEach(transaction => {
                        transactionHTML += `
                            <div class="transaction-block">
                                <h4>ID: ${transaction.ID}</h4>
                                <p><strong>Amount:</strong> ${transaction.Amount.toLocaleString()} VND</p>
                                <p><strong>Payment Method:</strong> ${transaction["Payment Method"]}</p>
                                <p><strong>Date:</strong> ${transaction["Transaction Date"]}</p>
                                <p><strong>Description:</strong> ${transaction.Description || "N/A"}</p>
                            </div>
                        `;
                    });
                } else {
                    transactionHTML += `<p>No sent transactions.</p>`;
                }

                transactionHTML += `</div><div class="transaction-column"><h3>Received Transactions</h3>`;

                if (data.receives && data.receives.length > 0) {
                    data.receives.forEach(receive => {
                        transactionHTML += `
                            <div class="transaction-block">
                                <h4>ID: ${receive.ID}</h4>
                                <p><strong>Amount:</strong> ${receive.Amount.toLocaleString()} VND</p>
                                <p><strong>Payment Method:</strong> ${receive["Payment Method"]}</p>
                                <p><strong>Date:</strong> ${receive["Transaction Date"]}</p>
                                <p><strong>Description:</strong> ${receive.Description || "N/A"}</p>
                            </div>
                        `;
                    });
                } else {
                    transactionHTML += `<p>No received transactions.</p>`;
                }

                transactionHTML += `</div></div>`;
                homeSection.innerHTML = transactionHTML;
            } else {
                homeSection.innerHTML = `
                    <div class="title">Transactions</div>
                    <p style="margin-left: 30px;">No transactions found.</p><br><br>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching transactions:", error);
            homeSection.innerHTML = `
                <div class="title">Transactions</div>
                <p>Error loading transactions.</p>
            `;
        });
}


    function loadCustomer() {
    fetch('/get-customer')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success" && data.customers.length > 0) {
                let customersHTML = `
                    <div class="title">Manage Customer</div>
                    <div class="features-container">
                        <input type="text" id="customerSearch" class="search-box" placeholder="Search by name, phone, username..." />
                        <div class="account-container">
                            <table id="accountTable" class="account-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Phone</th>
                                        <th>Username</th>
                                        <th>Gender</th>
                                        <th>Birth</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody id="accountTableBody">
                                </tbody>
                            </table>
                            <a href="/register">
                                <div class="add">
                                    <i class='bx bx-plus' ></i>
                                    <span class="add-text">Add Customer</span>
                                </div>
                            </a>
                        </div>
                    </div>
                `;

                homeSection.innerHTML = customersHTML;

                const tableBody = document.getElementById("accountTableBody");

                data.customers.forEach(customer => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${customer.id}</td>
                        <td>${customer.name}</td>
                        <td>${customer.phone}</td>
                        <td>${customer.username}</td>
                        <td>${customer.gender}</td>
                        <td>${customer.birth}</td>
                        <td class="edit-box"><a href="/manage-customer/${customer.id}">Edit</a></td>
                    `;
                    tableBody.appendChild(row);
                });

                // Search filter logic
                const searchInput = document.getElementById("customerSearch");
                searchInput.addEventListener("input", function () {
                    const keyword = this.value.toLowerCase();
                    const rows = tableBody.getElementsByTagName("tr");
                    Array.from(rows).forEach(row => {
                        const text = row.innerText.toLowerCase();
                        row.style.display = text.includes(keyword) ? "" : "none";
                    });
                });

            } else {
                homeSection.innerHTML = `
                    <div class="title">Manage Customer</div>
                    <p>No customer found.</p><br><br>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching customers:", error);
            const homeSection = document.getElementById('homeSection');
            homeSection.innerHTML = `
                <div class="title">Manage Customer</div>
                <p>Lỗi khi tải khách hàng.</p>
            `;
        });
}



    function loadStaff() {
    fetch('/get-staff')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success" && data.accounts.length > 0) {
                let accountsHTML = `
                    <div class="title">Manage Staff</div>
                    <div class="features-container">
                        <input type="text" id="accountSearch" class="search-box" placeholder="Search by name, phone, username..." />
                        <div class="account-container">
                            <table id="accountTable" class="account-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Phone</th>
                                        <th>Username</th>
                                        <th>Gender</th>
                                        <th>Birth</th>
                                        <th>Access</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody id="accountTableBody">
                                </tbody>
                            </table>
                            <a href="/add-staff">
                                <div class="add">
                                    <i class='bx bx-plus' ></i>
                                    <span class="add-text">Add Staff</span>
                                </div>
                            </a>
                        </div>
                    </div>
                `;

                homeSection.innerHTML = accountsHTML;

                const tableBody = document.getElementById("accountTableBody");

                data.accounts.forEach(account => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${account.id}</td>
                        <td>${account.name}</td>
                        <td>${account.phone}</td>
                        <td>${account.username}</td>
                        <td>${account.gender}</td>
                        <td>${account.birth}</td>
                        <td>${account.access}</td>
                        <td class="edit-box"><a href="/manage-staff/${account.id}">Edit</a></td>
                    `;
                    tableBody.appendChild(row);
                });

                // Search filter logic
                const searchInput = document.getElementById("accountSearch");
                searchInput.addEventListener("input", function () {
                    const keyword = this.value.toLowerCase();
                    const rows = tableBody.getElementsByTagName("tr");
                    Array.from(rows).forEach(row => {
                        const text = row.innerText.toLowerCase();
                        row.style.display = text.includes(keyword) ? "" : "none";
                    });
                });

            } else {
                homeSection.innerHTML = `
                    <div class="title">Manage Staff</div>
                    <p>No staff found.</p><br><br>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching customers:", error);
            const homeSection = document.getElementById('homeSection');
            homeSection.innerHTML = `
                <div class="title">Manage Staff</div>
                <p>Error loading Staff.</p>
            `;
        });
}


    function loadCard() {
    fetch('/profile')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const account = data.account;
                const barcodeValue = `${account.ID}-${account.Phone}`;

                homeSection.innerHTML = `
                    <div class="title">My membership card</div>
                    <div class="user-info">
                        <h3 style="margin-bottom: 20px;">Print preview:</h3>
                        <div class="membership-card">
                            <div class="card-head">
                            <p>D-Cross Fitness: Membership Card</p>
                            </div>
                            <div class="card-body">
                                <div class="picture-icon"><i class='bx bx-user-circle' ></i></div>
                                <div class="card-info">
                                    <p><strong>Name:</strong> ${account.Name}</p>
                                    <p><strong>ID:</strong> ${account.ID}</p>
                                    <p><strong>Birth:</strong> ${account.Birth || "N/A"}</p>
                                    <svg id="barcode"></svg>
                                </div>
                            </div>
                        </div>
                        <form action="/request-print" class="btn-container-wide" method="POST">
                            <button type="submit" class="btn-wide btn-submit">Request Print</button>
                        </form>
                    </div>
                `;

                JsBarcode("#barcode", barcodeValue, {
                    format: "CODE128",
                    width: 2,
                    height: 50,
                    displayValue: false
                });
            } else {
                homeSection.innerHTML = `<div class="text">Error</div><p>${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
            homeSection.innerHTML = `<div class="text">Error</div><p>Failed to load user data.</p>`;
        });
}

    function loadSchedule() {
    fetch('/api/schedule')
        .then(res => res.json())
        .then(data => {
            const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            // Khởi tạo các mảng để chứa lịch làm việc cho mỗi ngày
            const scheduleByDay = {
                'Monday': [],
                'Tuesday': [],
                'Wednesday': [],
                'Thursday': [],
                'Friday': [],
                'Saturday': [],
                'Sunday': []
            };

            // Phân loại lịch theo ngày
            data.forEach(item => {
                scheduleByDay[item.Day].push(`Start: ${item.Start}<br>End: ${item.End}`);
            });

            let scheduleHTML = `
                <div class="title">Weekly Schedule</div>
                <div class="schedule-container">
                    <table class="schedule-table">
                        <thead>
                            <tr>
                                ${daysOfWeek.map(day => `<th>${day}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                ${daysOfWeek.map(day => {
                                    // Kiểm tra nếu có lịch cho ngày đó, nếu có thì thêm màu nền
                                    const hasSchedule = scheduleByDay[day].length > 0;
                                    return `
                                        <td class="${hasSchedule ? 'has-schedule' : ''}">
                                            ${hasSchedule ? scheduleByDay[day].join('<br>') : '—'}
                                        </td>
                                    `;
                                }).join('')}
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;

            homeSection.innerHTML = scheduleHTML;
        })
        .catch(err => {
            console.error("Error loading schedule data:", err);
            homeSection.innerHTML = `<p>Error loading schedule data.</p>`;
        });
}


function loadClassSchedules() {
    fetch('/api/class-info')
        .then(res => res.json())
        .then(data => {
            if (!data || (Array.isArray(data) && data.length === 0)) {
                homeSection.innerHTML = '<p>No class schedules found.</p>';
                return;
            }

            let currentUserClassID = null;

            // Nếu response là object đơn (khách đã có lớp)
            if (!Array.isArray(data)) {
                currentUserClassID = data.Class?.idClass;
                data = [data]; // chuyển thành mảng để duyệt
            }

            // Kiểm tra nếu account đã có lớp
            const title = currentUserClassID ? 'My Class' : 'Classes Info';

            let table = `
                <div class="title">${title}</div>
                <div class="schedule-container">
                    <table class="schedule-table">
                        <thead>
                            <tr>
                                <th>Class Info</th>
                                <th>Monday</th>
                                <th>Tuesday</th>
                                <th>Wednesday</th>
                                <th>Thursday</th>
                                <th>Friday</th>
                                <th>Saturday</th>
                                <th>Sunday</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            data.forEach(entry => {
                const classInfo = entry.Class;
                const trainer = entry.Trainer;
                const schedules = entry.Schedule;

                let row = `<tr><td class="class-info">
                    <strong>${classInfo.Name}</strong><br>
                    Trainer: ${trainer.Name}<br>
                    Phone: ${trainer.Phone}<br>`;

                if (parseInt(currentUserClassID) === classInfo.idClass) {
                    row += `<a href="/unenroll-form" class="action-btn"><div class="btn-enroll">Unenroll</div></a>`;
                } else {
                    row += `<a href="/enroll-form?idClass=${classInfo.idClass}" class="action-btn"><div class="btn-enroll">Enroll</div></a>`;
                }

                row += `</td>`;

                days.forEach(day => {
                    const daySchedules = schedules.filter(s => s.Day === day);
                    if (daySchedules.length > 0) {
                        const scheduleHTML = daySchedules.map(s => `
                            Start: <br>${s.Start}<br><br>
                            End: <br>${s.End}
                        `).join('<hr>');
                        row += `<td class="has-schedule">${scheduleHTML}</td>`;
                    } else {
                        row += `<td></td>`;
                    }
                });

                row += `</tr>`;
                table += row;
            });

            table += `</tbody></table></div>`;
            homeSection.innerHTML = table;
        })
        .catch(error => {
            console.error('Error loading class data', error);
            homeSection.innerHTML = '<p>Error loading class data.</p>';
        });
}

function loadClassList() {
    fetch('/api/class-info')
        .then(res => res.json())
        .then(data => {
            if (!data || (Array.isArray(data) && data.length === 0)) {
                homeSection.innerHTML = '<p>No class schedules found.</p>';
                return;
            }

            let currentUserClassID = null;


            if (!Array.isArray(data)) {
                currentUserClassID = data.Class?.idClass;
                data = [data];
            }



            let table = `
                <div class="title">Classes</div>

                <div class="schedule-container" style="margin-left: 60px;">
                <a href="/class-manage-form" class="btn-wide btn-submit">Manage</a>
                    <table class="schedule-table">
                        <thead>
                            <tr>
                                <th>Class Info</th>
                                <th>Monday</th>
                                <th>Tuesday</th>
                                <th>Wednesday</th>
                                <th>Thursday</th>
                                <th>Friday</th>
                                <th>Saturday</th>
                                <th>Sunday</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            data.forEach(entry => {
                const classInfo = entry.Class;
                const trainer = entry.Trainer;
                const schedules = entry.Schedule;

                let row = `<tr><td class="class-info">
                    <strong>${classInfo.Name}</strong><br>
                    Trainer: ${trainer.Name}<br>
                    Phone: ${trainer.Phone}<br>`;


                days.forEach(day => {
                    const daySchedules = schedules.filter(s => s.Day === day);
                    if (daySchedules.length > 0) {
                        const scheduleHTML = daySchedules.map(s => `
                            Start: <br>${s.Start}<br><br>
                            End: <br>${s.End}
                        `).join('<hr>');
                        row += `<td class="has-schedule">${scheduleHTML}</td>`;
                    } else {
                        row += `<td></td>`;
                    }
                });

                row += `</tr>`;
                table += row;
            });

            table += `</tbody></table></div>`;
            homeSection.innerHTML = table;
        })
        .catch(error => {
            console.error('Error loading class data', error);
            homeSection.innerHTML = '<p>Error loading class data.</p>';
        });
}


function loadTrainerClass() {
    fetch('/trainer/my-class')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const classInfo = data.class;
                const students = data.students;

                const studentRows = students.map(student => `
                    <tr>
                        <td class="check-cell custom-checkbox">
                            <input type="checkbox" name="present_ids" value="${student.idAccount}" style="width: 20px; height: 20px;" checked>
                        </td>
                        <td>${student.idAccount}</td>
                        <td>${student.Name}</td>
                        <td>${student.Phone}</td>
                        <td class="edit-box">
                            <a href="/removeStudent/${student.idAccount}">Remove</a>
                        </td>
                    </tr>
                `).join('');

                homeSection.innerHTML = `
                    <div class="title">My Class - ${classInfo.Name}</div>
                    <div class="features-container">
                        <div class="table-wrapper">
                            <form action="/trainer/attendance" method="post">
                                <table class="account-table">
                                    <thead>
                                        <tr>
                                            <th>Attend</th>
                                            <th>ID</th>
                                            <th>Name</th>
                                            <th>Phone</th>
                                            <th></th>
                                        </tr>
                                    </thead>
                                    <tbody>${studentRows}</tbody>
                                </table>
                                <button type="submit" class="btn-wide btn-submit" style="width: 800px">Submit Attendance</button>
                            </form>
                        </div>
                    </div>
                `;
            } else {
                homeSection.innerHTML = `<p>${data.message}</p>`;
            }
        });
}


function loadEquipmentBoard() {
    fetch('/equipment')  // Đảm bảo URL này đúng với route trên server
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Kiểm tra dữ liệu trả về từ API

            if (data.status === "success" && data.equipment.length > 0) {
                let equipmentHTML = `
                    <div class="title">Manage Equipment</div>
                    <div class="features-container">
                        <input type="text" id="equipmentSearch" class="search-box" placeholder="Search by name, Category, Brand..." />
                        <div class="account-container">
                            <table id="equipmentTable" class="account-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Brand</th>
                                        <th>Category</th>
                                        <th>Quantity</th>
                                        <th>Available</th>
                                        <th>Size</th>
                                        <th>Weight</th>
                                        <th>Image</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody id="equipmentTableBody">
                                </tbody>
                            </table>
                            <a href="/add-equipment">
                                <div class="add">
                                    <i class='bx bx-plus' ></i>
                                    <span class="add-text">Add Equipment</span>
                                </div>
                            </a>
                        </div>
                    </div><br>
                `;

                homeSection.innerHTML = equipmentHTML;  // Cập nhật nội dung vào homeSection

                const tableBody = document.getElementById("equipmentTableBody");

                data.equipment.forEach(equipment => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${equipment.ID}</td>
                        <td>${equipment.Name}</td>
                        <td>${equipment.Brand}</td>
                        <td>${equipment.Category}</td>
                        <td>${equipment.Quantity}</td>
                        <td>${equipment["Quantity Available"]}</td>
                        <td>${equipment.Size}</td>
                        <td>${equipment.Weight}</td>
                        <td><img src="${equipment.Image}" alt="Equipment Image" width="100"></td>
                        <td class="edit-box"><a href="/manage-equipment/${equipment.ID}">Edit</a></td>
                    `;
                    tableBody.appendChild(row);
                });

                const searchInput = document.getElementById("equipmentSearch");
                searchInput.addEventListener("input", function () {
                    const keyword = this.value.toLowerCase();
                    const rows = tableBody.getElementsByTagName("tr");
                    Array.from(rows).forEach(row => {
                        const text = row.innerText.toLowerCase();
                        row.style.display = text.includes(keyword) ? "" : "none";
                    });
                });
            } else {
                homeSection.innerHTML = `<div class="title">Manage Equipment</div><p>No equipment found.</p><br><br>`;
            }
        })
        .catch(error => {
            console.error("Error fetching equipment:", error);
            homeSection.innerHTML = `<div class="title">Manage Equipment</div><p>Error loading equipment.</p>`;
        });
}


function loadRevenueStats() {
    fetch('/profile')
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                homeSection.innerHTML = `<p>Error loading revenue stats.</p>`;
                return;
            }

            const allTransactions = [...data.transactions, ...data.receives.map(r => ({ ...r, isReceive: true }))];

            const monthlyStats = {};
            allTransactions.forEach(tx => {
                const date = new Date(tx["Transaction Date"]);
                const month = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;
                const amount = tx.Amount;

                if (!monthlyStats[month]) monthlyStats[month] = { income: 0, expense: 0 };
                if (tx.isReceive) {
                    monthlyStats[month].income += amount;
                } else {
                    monthlyStats[month].expense += amount;
                }
            });

            const sortedMonths = Object.keys(monthlyStats).sort().reverse();
            const latestFour = sortedMonths.slice(0, 4);
            const statsToShow = latestFour.reverse();

            const tableRows = statsToShow.map(month => {
                const { income, expense } = monthlyStats[month];
                return `
                    <tr>
                        <td>${month}</td>
                        <td>${income.toLocaleString()} VND</td>
                        <td>${expense.toLocaleString()} VND</td>
                        <td>${(income - expense).toLocaleString()} VND</td>
                    </tr>`;
            }).join('');

            const totalIncome = statsToShow.reduce((sum, m) => sum + monthlyStats[m].income, 0);
            const totalExpense = statsToShow.reduce((sum, m) => sum + monthlyStats[m].expense, 0);

            homeSection.innerHTML = `
                <div class="title">Revenue Statistics</div>
                <div style="display: flex; gap: 30px; margin: 20px auto; width: 1000px;">
                    <div style="flex: 2; width: 600px;">
                        <table class="table membership-table">
                            <thead>
                                <tr>
                                    <th>Month</th>
                                    <th>Income</th>
                                    <th>Expense</th>
                                    <th>Net</th>
                                </tr>
                            </thead>
                            <tbody>${tableRows}</tbody>
                        </table>
                        <div style="margin-top: 10px;">
                            <strong>Total Income:</strong> ${totalIncome.toLocaleString()} VND |
                            <strong>Total Expense:</strong> ${totalExpense.toLocaleString()} VND |<br>
                            <strong>Net:</strong> ${(totalIncome - totalExpense).toLocaleString()} VND
                        </div>
                        <div class="btn-container-wide">
                            <a href="/revenue" class="btn btn-wide btn-submit">Show Detail</a>
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <canvas id="revenueChart" height="250"></canvas>
                    </div>
                </div>
            `;

            const ctx = document.getElementById('revenueChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: statsToShow,
                    datasets: [
                        {
                            label: 'Income',
                            data: statsToShow.map(m => monthlyStats[m].income),
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        },
                        {
                            label: 'Expense',
                            data: statsToShow.map(m => monthlyStats[m].expense),
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Monthly Revenue Summary' }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error:", error);
            homeSection.innerHTML = `<p>Error loading revenue stats.</p>`;
        });
}








    document.addEventListener("click", function (e) {
        const target = e.target.closest("[data-content]");
        if (target) {
            e.preventDefault();
            const content = target.getAttribute("data-content");

            if (content === "Membership") {
                loadMembershipContent();
            } else if (content === "ManageCustomer") {
                loadCustomer();
            } else if (content === "User") {
                loadUserProfile();
            } else if (content === "Dashboard") {
                loadDashboardContent();
            } else if (content === "Transactions") {
                loadTransactionsContent();
            } else if (content === "Card") {
                loadCard();
            } else if (content === "MySchedule") {
                loadSchedule();
            } else if (content === "Classes") {
                loadClassSchedules();
            } else if (content === "ManageClass") {
                loadTrainerClass();
            } else if (content === "ManageEquipment") {
                loadEquipmentBoard();
            } else if (content === "Financial") {
                loadRevenueStats();
            } else if (content === "ManageStaff") {
                loadStaff();
            } else if (content === "ManageClasses") {
                loadClassList();
            }
        }
    });

    loadDashboardContent();
});
