package main

import (
	"bufio"
	"fmt"
	"os"
)

var (
	grid          [][]rune
	WIDTH, HEIGHT int
	NEXT_CHAR     = map[rune]rune{'X': 'M', 'M': 'A', 'A': 'S'}
	// Neighbours (Square)
	ADJ = [][2]int{
		{-1, -1}, {0, -1}, {1, -1},
		{-1, 0}, {1, 0},
		{-1, 1}, {0, 1}, {1, 1},
	}
	// Neighbours (X-shape)
	ADJ_X = [][2]int{
		{-1, -1}, {1, -1},
		{-1, 1}, {1, 1},
	}
	VALID_NEIGHBOUR_STRINGS = map[string]bool{
		"SSMM": true,
		"MSMS": true,
		"SMSM": true,
		"MMSS": true,
	}
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) > 0 {
			grid = append(grid, []rune(line))
		}
	}

	HEIGHT, WIDTH = len(grid), len(grid[0])

	// Part 1
	totalXmas := part1()
	fmt.Println(totalXmas) // 2358

	// Part 2
	xMasCount := part2()
	fmt.Println(xMasCount) // 1737
}

func part1() int {
	xPositions := findPositions('X')
	queue := make([][4]interface{}, len(xPositions))
	copy(queue, xPositions)
	totalXmas := 0

	for len(queue) > 0 {
		pos := queue[0]
		queue = queue[1:]
		neighbours := getValidNeighbours(pos)

		for _, n := range neighbours {
			if n[2].(rune) == 'S' {
				totalXmas++
			} else {
				queue = append(queue, n)
			}
		}
	}

	return totalXmas
}

func part2() int {
	aPositions := findPositions('A')
	xMasCount := 0

	for _, pos := range aPositions {
		x, y := pos[0].(int), pos[1].(int)
		neighbourStr := ""

		for _, adj := range ADJ_X {
			nx, ny := x+adj[0], y+adj[1]
			if nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT {
				char := grid[ny][nx]
				if char == 'M' || char == 'S' {
					neighbourStr += string(char)
				}
			}
		}

		if len(neighbourStr) == 4 && VALID_NEIGHBOUR_STRINGS[neighbourStr] {
			xMasCount++
		}
	}

	return xMasCount
}

func findPositions(target rune) [][4]interface{} {
	positions := [][4]interface{}{}
	for y := 0; y < HEIGHT; y++ {
		for x := 0; x < WIDTH; x++ {
			if grid[y][x] == target {
				positions = append(positions, [4]interface{}{x, y, target, nil})
			}
		}
	}
	return positions
}

func getValidNeighbours(pos [4]interface{}) [][4]interface{} {
	x, y := pos[0].(int), pos[1].(int)
	char := pos[2].(rune)
	dir := pos[3]

	neighbours := [][4]interface{}{}
	adj := ADJ
	if dir != nil {
		d := dir.([2]int)
		adj = [][2]int{d}
	}

	for _, d := range adj {
		nx, ny := x+d[0], y+d[1]
		if nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT {
			newChar := grid[ny][nx]
			if newChar == NEXT_CHAR[char] {
				neighbours = append(neighbours, [4]interface{}{nx, ny, newChar, d})
			}
		}
	}

	return neighbours
}
