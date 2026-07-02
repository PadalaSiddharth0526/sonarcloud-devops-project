import { useState } from 'react';
import { add } from './utils/math.js';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app">
      <h1>SonarCloud CI/CD Demo</h1>
      <p data-testid="count-display">Count: {count}</p>
      <button onClick={() => setCount(add(count, 1))}>Increment</button>
    </div>
  );
}

export default App;
