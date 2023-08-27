// Check if the counter value is stored in local storage
let counterValue = localStorage.getItem('refreshCounter');

// If counter value is not present, initialize it to 0
if (!counterValue) {
    counterValue = 0;
}

// Increment the counter value
counterValue = parseInt(counterValue) + 1;

// Store the updated counter value in local storage
localStorage.setItem('refreshCounter', counterValue);

// Log the updated counter value to the console
console.log('Visit Counter:', counterValue);