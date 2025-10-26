// Wait for the HTML document to finish loading
document.addEventListener('DOMContentLoaded', function() {
  
  // Find the elements we need
  const portionInput = document.getElementById('portion-input');
  const ingredientList = document.getElementById('ingredient-list');
  
  // Check if we are on a page that actually has these elements
  if (portionInput && ingredientList) {
    
    // Get the original serving size from the <ul>'s data attribute
    const defaultServings = parseFloat(ingredientList.dataset.defaultServings);
    
    // Find all the <li> items in the ingredient list
    const listItems = ingredientList.querySelectorAll('li');
    
    // This function calculates and updates the quantities
    function updateQuantities() {
      // Get the new serving size the user entered
      const newServings = parseFloat(portionInput.value);

      // Make sure it's a valid, positive number
      if (isNaN(newServings) || newServings <= 0) {
        return;
      }
      
      // Calculate the multiplication factor
      const multiplier = newServings / defaultServings;
      
      // Loop through each ingredient <li>
      listItems.forEach(item => {
        // Get the original quantity from its data attribute
        const baseQuantity = parseFloat(item.dataset.baseQuantity);
        
        // Find the <span> where the number is displayed
        const quantitySpan = item.querySelector('.quantity');
        
        // Calculate the new quantity
        let newQuantity = baseQuantity * multiplier;
        
        // Round to 2 decimal places to avoid long numbers (e.g., 0.333333)
        // Math.round(num * 100) / 100 is a good trick for this.
        let displayQuantity = Math.round(newQuantity * 100) / 100;

        // Update the text in the <span>
        quantitySpan.textContent = displayQuantity;
      });
    }

    // Add an 'event listener' that calls our update function
    // every time the user types in the input box.
    portionInput.addEventListener('input', updateQuantities);
  }
});