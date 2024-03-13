import logo from './logo.svg';
import './App.css';

import { useState } from 'react';

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board({ xIsNext, squares, onPlay, currentMove}) {

  const [prevState, setPrevState] = useState(-1);
  const [prevSquares, setPrevSquares] = useState([]);
  const [xMiddle, setXMiddle] = useState(false);
  const [oMiddle, setOMiddle] = useState(false);

  function handleClick(i) {
    const nextSquares = squares.slice();

    // cool we are gonna play lapis lazulli
    if (currentMove >= 6){
      
      
      if (squares[i] === null && prevState !== -1){
        console.log(prevState);
        if (validMove(i, prevState) || prevState === i) {

          if (xIsNext) nextSquares[i] = 'X';
          else nextSquares[i] = 'O';

          if (i === prevState) {
            onPlay(prevSquares);
          }
          else onPlay(nextSquares)
        }
        else return;
        setPrevState(-1);
        setXMiddle(false);
        setOMiddle(false);
       
      }

      else { 

      if (squares[4] === 'X') setXMiddle(true);
      if (squares[4] === 'O') setOMiddle(true);


      if ((squares[i] === 'X' && xIsNext) || (squares[i] === 'O' && !xIsNext)) {
         setPrevSquares([...squares]);
          squares[i] = null;
          setPrevState(i);

      }
/*
  
      if (squares[i] === 4){
        squares[i] = xIsNext ? 'X' : 'O';
        if (!calculateWinner(squares)){
          squares[i] = 'null';
          return;
        }
      }
      
      squares[i] = null;
      if (xIsNext){
        nextSquares[i] = 'X';
      }
      else{
        nextSquares[i] = 'O';
      }
      
  */
    }
  }
    else{
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    
    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    onPlay(nextSquares);
  }


  }
  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }
   



  

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];
  function handlePlay(nextSquares) {
   const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
   setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = 'Go to move #' + move;
    } else {
      description = 'Go to game start';
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });


  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} currentMove ={currentMove}/>
      </div>
      <div className="game-info">
        <ol>{moves}</ol>
      </div>
    </div>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }


  return null;
}

function validMove(current, last){
  switch (current){
    case 0:
      return last===1||last===3||last===4;
    case 1:
      return last===0||last===2||last===3||last===4||last===5;
    case 2:
      return last===1||last===4||last===5;
    case 3:
      return last===0||last===1||last===4||last===6||last===7;
    case 4:
      //the character can always move to position 4
      return true;
    case 5:
      return last===1||last===2||last===4||last===7||last===8;
    case 6:
      return last===3||last===4||last===7;
    case 7:
      return last===3||last===4||last===5||last===6||last===8;
    case 8:
      return last===7||last===4||last===5;
    default:
      return;

  }

}
