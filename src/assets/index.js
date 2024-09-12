//filler data
const data = [
    'Apple',
    'Banana',
    'Cherry',
    'Date',
    'Elderberry',
    'Fig',
    'Grape',
    'Honeydew'
];

document.getElementById('search-button').addEventListener('click', function() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const filterValue = document.getElementById('filter-dropdown').value;
    const results = document.getElementById('results');

    // Clear previous results
    results.innerHTML = '';

    // Filter data
    const filteredData = data.filter(item => {
        const itemLower = item.toLowerCase();
        if (filterValue === 'all') {
            return itemLower.includes(searchInput);
        } else if (filterValue === 'uppercase') {
            return item === item.toUpperCase() && itemLower.includes(searchInput);
        } else if (filterValue === 'lowercase') {
            return item === item.toLowerCase() && itemLower.includes(searchInput);
        }
        return false;
    });

    // Display results
    filteredData.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item;
        results.appendChild(listItem);
    });
});



