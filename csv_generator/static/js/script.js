// Get the add button
const addButton = document.querySelector('.add-schema-button');

// Create a function to add new schema columns
const addSchemaColumn = () => {
// Create a new row for the schema column
const newRow = document.createElement('div');
newRow.classList.add('row', 'schema-column');

// Create the three inputs for the new row
const nameInput = document.createElement('input');
nameInput.type = 'text';
nameInput.classList.add('form-control', 'column-name');
nameInput.placeholder = 'Column Name';

const typeInput = document.createElement('input');
typeInput.type = 'text';
typeInput.classList.add('form-control', 'column-type');
typeInput.placeholder = 'Column Type';

const orderInput = document.createElement('input');
orderInput.type = 'number';
orderInput.classList.add('form-control', 'column-order');
orderInput.placeholder = 'Column Order';

// Append the inputs to the new row
newRow.appendChild(nameInput);
newRow.appendChild(typeInput);
newRow.appendChild(orderInput);

// Append the new row to the container
const container = document.querySelector('.schema-columns-container');
container.appendChild(newRow);
};

// Listen for a click on the add button
addButton.addEventListener('click', addSchemaColumn);


