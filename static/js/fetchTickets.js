// document.addEventListener('DOMContentLoaded', function() {
//     const filters = document.querySelectorAll('.filter-btn');
//     filters.forEach(filter => {
//         filter.addEventListener('click', function() {
//             const filter_by = this.dataset.filter;
//             fetchTickets(filter_by);
//         });
//     });
// });

// function fetchTickets(filter_by) {
//     const limit = 10;  // Default limit
//     fetch(`/tickets/fetch-tickets?filter_by=${filter_by}&limit=${limit}`, {
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         updateTicketList(data.tickets);
//     });
// }

// function updateTicketList(tickets) {
//     const ticketListContainer = document.getElementById('ticket-list-container');
//     ticketListContainer.innerHTML = '';
//     tickets.forEach(ticket => {
//         const ticketElement = document.createElement('li');
//         ticketElement.className = 'mb-2 p-2 bg-gray-100 rounded shadow';
//         ticketElement.innerHTML = `<p><strong>Subject:</strong> ${ticket.subject}</p>
//                                    <p><strong>External ID:</strong> ${ticket.external_id}</p>`;
//         ticketListContainer.appendChild(ticketElement);
//     });
// }
