<h1>Chess CLI</h1>

<p>A command line interface for playing chess and generating FEN strings</p>

<h2>Prerequisites</h2>

<p>None. This project is compiled as a plug and play .exe file. Database access is not required</p>

<p>The .exe file is available from the dist folder or from https://liambell.info/files/chess-cli.exe</p>

<h2>Commands</h2>

<p>
	The following commands are available when running the app:

	<ul>
		<li>help: prints a list of the available commands (as shown below)</li>
		<li>load_position: Provide a FEN to load a game from that position</li>
		<li>make_move: Make a move. Provide the move in uci format e.g. e2e4 d7d8q</li>
		<li>print_board: Print a representation of the board. Dots are empty squares, capital letters are white pieces</li>
		<li>print_fen: Print the FEN for the current position in the game</li>
		<li>print_move_notation: Print the algebraic notation for a move in uci format. This does not actually make the move</li>
		<li>print_game_state: Prints whether the game is checkmate, stalemate, or else which colour is next to move</li>
	</ul>
</p>