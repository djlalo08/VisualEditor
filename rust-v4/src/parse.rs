use crate::{
    builtins::{BUILTIN_FNS, SPECIAL_BUILTIN_FNS},
    log,
    runtime_types::{ArgOrder, Dag, InputIndex, Node, NodeIndex, OutputIndex, ScopeIdx, Value},
};
use std::io::Write;
use std::{
    collections::{HashSet, VecDeque},
    fs, usize,
};

type OutInMap = String;
type Pos = (usize, usize); // x, y

#[derive(Debug)]
pub enum ParseError {
    Io(std::io::Error),
    Regex(regex::Error),
    BoxVerticalLineExceededGridBounds,
    UnexpectedBoxChar { ch: char, col: usize, row: usize },
    Other(String),
}

impl From<std::io::Error> for ParseError {
    fn from(e: std::io::Error) -> Self {
        ParseError::Io(e)
    }
}

impl From<regex::Error> for ParseError {
    fn from(e: regex::Error) -> Self {
        ParseError::Regex(e)
    }
}

pub(crate) fn parse(file: &str) -> Result<Vec<Dag>, ParseError> {
    let contents = fs::read_to_string(file)?;
    let lines: Vec<&str> = contents.lines().collect();
    let grid = create_grid(&lines);
    let mut tokens: Vec<Token> = Vec::new();
    let mut boxes: Vec<Box> = Vec::new();

    for (row, data) in lines.iter().enumerate() {
        let row = row + 1;
        let data = *data;
        if data.starts_with("//") || data.trim().is_empty() {
            continue;
        }
        boxes.extend(parse_box_tops(data, row, &grid)?);
        tokens.extend(find_tokens(data, row)?);
    }
    tokens.retain(|t| !boxes.iter().any(|b| b.name == t.name));

    print(&boxes, &tokens);

    let mut dags = vec![];
    // For every box, find tokens inside it
    // Note: This assumes boxes are non-overlapping
    // and that tokens are not inside top-level scope
    for (box_num, box_item) in boxes.iter().enumerate() {
        let inside_tokens: Vec<&Token> = tokens.iter().filter(|t| is_inside(t, box_item)).collect();
        let nodes: Vec<Node> = inside_tokens
            .iter()
            .map(|t| token_to_node(t, &tokens, box_num))
            .collect();
        let edges = inside_tokens
            .iter()
            .map(|t| follow_paths(t, &grid, &tokens).unwrap())
            .map(sort_and_map_inputs)
            .collect();
        print_edges(&edges, &tokens);
        let graph = Dag {
            nodes: nodes,
            edges: edges,
        };
        dags.push(graph);
    }

    Ok(dags)
}

fn sort_and_map_inputs(inputs: Vec<(TokenIndex, String)>) -> Vec<(NodeIndex, OutputIndex)> {
    let mut inputs = inputs
        .iter()
        .flat_map(|(input_token_idx, map)| {
            parse_out_in_map(map)
                .iter()
                .map(|(input_idx, output_idx)| (*input_token_idx, *output_idx, *input_idx))
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    inputs.sort_by_key(|(_, _, input_index)| input_index.0);
    inputs
        .iter()
        .map(|(token_idx, output_idx, _)| (NodeIndex(token_idx.0), *output_idx))
        .collect()
}

fn parse_out_in_map(map: &str) -> Vec<(InputIndex, OutputIndex)> {
    map.trim()
        .strip_prefix(":")
        .unwrap()
        .split(',')
        .map(|mapping| {
            let (output, input) = mapping
                .trim()
                .split_once("->")
                .expect(&format!("Invalid mapping format, {mapping}"));
            let output_idx = output
                .trim()
                .parse::<usize>()
                .expect("Invalid output index");
            // Note that this assumes mappings look like 1->2 and does not handle 1:2->3
            // TODO: Handle nested mappings
            let input_idx = input.trim().parse::<usize>().expect("Invalid input index");
            (InputIndex(input_idx - 1), OutputIndex(output_idx - 1))
        })
        .collect()
}

fn is_inside(token: &Token, bx: &Box) -> bool {
    let token_pos = &token.position;
    let box_pos = &bx.position;
    token_pos.bottom_left.0 >= box_pos.bottom_left.0
        && token_pos.top_right.0 <= box_pos.top_right.0
        && token_pos.bottom_left.1 <= box_pos.bottom_left.1
        && token_pos.top_right.1 >= box_pos.top_right.1
}

fn find_out_in_map(
    token: &Token,
    char_grid: &Vec<Vec<char>>,
    valid_path: &HashSet<Pos>,
) -> Result<OutInMap, ParseError> {
    let x0 = token.position.bottom_left.0;
    let xf = token.position.top_right.0;
    let y = token.position.bottom_left.1;

    let bottoms = (x0..=xf).map(|x| (x, y + 1));
    let starting_positions: VecDeque<_> = VecDeque::from([(x0 - 1, y), (xf + 1, y)])
        .into_iter()
        .chain(bottoms)
        .collect();

    let mut queue = starting_positions;
    while let Some((x, y)) = queue.pop_front() {
        let width = char_grid[y].len();

        // Bounds check
        if y == 0 || y >= char_grid.len() || x == 0 || x >= width {
            continue;
        }
        let ch = char_grid[y][x];

        if ch == '┃' && char_grid[y][x + 1] == ':' {
            return Ok(char_grid[y][(x + 1)..width]
                .iter()
                .take_while(|&&c| c != ' ')
                .collect::<String>());
        }

        // Otherwise, keep following the path
        for (nx, ny) in steps_down(char_grid, (x, y)) {
            if valid_path.contains(&(nx, ny)) {
                queue.push_back((nx, ny));
            }
        }
    }
    Err(ParseError::Other(format!(
        "No valid out-in map found for token {}",
        token.name
    )))
}

fn follow_paths(
    token: &Token,
    char_grid: &Vec<Vec<char>>,
    tokens: &[Token],
) -> Result<Vec<(TokenIndex, OutInMap)>, ParseError> {
    let x0 = token.position.bottom_left.0;
    let xf = token.position.top_right.0;
    let y = token.position.bottom_left.1;

    let (left_ins, path) =
        follow_paths_dir(token, char_grid, tokens, VecDeque::from([(x0 - 1, y)]))?;
    let left_ins: Vec<_> = left_ins
        .iter()
        .map(|t_i| {
            (
                *t_i,
                find_out_in_map(&tokens[t_i.0], char_grid, &path).unwrap(),
            )
        })
        .collect();

    let aboves = (x0..=xf).map(|x| (x, y - 1));
    let (above_ins, path) =
        follow_paths_dir(token, char_grid, tokens, VecDeque::from_iter(aboves))?;
    let mut above_ins = above_ins
        .iter()
        .map(|t_i| {
            (
                *t_i,
                find_out_in_map(&tokens[t_i.0], char_grid, &path).unwrap(),
            )
        })
        .collect();

    let (right_ins, path) =
        follow_paths_dir(token, char_grid, tokens, VecDeque::from([(xf + 1, y)]))?;
    let mut right_ins: Vec<_> = right_ins
        .iter()
        .map(|t_i| {
            (
                *t_i,
                find_out_in_map(&tokens[t_i.0], char_grid, &path).unwrap(),
            )
        })
        .collect();

    let mut result = left_ins;
    result.append(&mut above_ins);
    result.append(&mut right_ins);
    Ok(result)
}

fn follow_paths_dir(
    token: &Token,
    char_grid: &Vec<Vec<char>>,
    tokens: &[Token],
    starting_positions: VecDeque<Pos>,
) -> Result<(Vec<TokenIndex>, HashSet<Pos>), ParseError> {
    let mut found_indices = Vec::new();
    let mut visited = HashSet::new();
    let mut queue = starting_positions;

    // Mark all positions of the token itself as visited so it can't visit itself
    let y = token.position.bottom_left.1;
    let x0 = token.position.bottom_left.0;
    let xf = token.position.top_right.0;
    for x in x0..=xf {
        visited.insert((x, y));
    }

    while let Some((x, y)) = queue.pop_front() {
        if !visited.insert((x, y)) {
            continue;
        }
        // Bounds check
        if y == 0 || y >= char_grid.len() || x == 0 || x >= char_grid[y].len() {
            continue;
        }
        let ch = char_grid[y][x];

        // If not a symbol, check if it's part of a token (alphanumeric or ':', '-', '_', '+')
        if !SYMBOLS.iter().any(|&s| s.chars().next().unwrap() == ch) {
            // If this position is part of any token, mark that token as found
            for (i, t) in tokens.iter().enumerate() {
                if t.position.bottom_left.1 == y
                    && t.position.bottom_left.0 <= x
                    && x <= t.position.top_right.0
                {
                    // Don't add the original token itself
                    if t.position.bottom_left != token.position.bottom_left
                        || t.position.top_right != token.position.top_right
                    {
                        found_indices.push(TokenIndex(i));
                    }
                    break;
                }
            }
            continue;
        }

        // Otherwise, keep following the path
        for (nx, ny) in steps_up(char_grid, (x, y)) {
            if !visited.contains(&(nx, ny)) {
                queue.push_back((nx, ny));
            }
        }
    }
    visited.retain(|&(x_vis, y_vis)| y != y_vis || x_vis < x0 || x_vis > xf);
    visited.retain(|&(x_vis, y_vis)| char_grid[y_vis][x_vis] != ' ');

    Ok((found_indices, visited))
}

fn safe_access(grid: &Vec<Vec<char>>, pos: Pos) -> Option<char> {
    let (x, y) = pos;
    if y > 0 && y < grid.len() && x > 0 && x < grid[y].len() {
        Some(grid[y][x])
    } else {
        None
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Copy)]
pub struct TokenIndex(pub usize);
impl Into<NodeIndex> for TokenIndex {
    fn into(self) -> NodeIndex {
        NodeIndex(self.0)
    }
}
impl From<usize> for TokenIndex {
    fn from(idx: usize) -> Self {
        TokenIndex(idx)
    }
}

//Only include steps that stay horizontal or move up (towards y = 0)
fn steps_up(grid: &Vec<Vec<char>>, pos: Pos) -> Vec<(Pos)> {
    let (x, y) = pos;
    match grid[y][x] {
        '┏' => vec![(x + 1, y)],
        '┓' => vec![(x - 1, y)],
        '┛' | '┗' => vec![(x, y - 1)],
        '┣' => vec![(x, y - 1), (x + 1, y)],
        '┫' => vec![(x - 1, y), (x, y - 1)],
        '┻' | '╋' => vec![(x - 1, y), (x, y - 1), (x + 1, y)],
        '┳' => vec![(x - 1, y), (x + 1, y)],
        '━' => vec![(x - 1, y), (x + 1, y)],
        '┃' => vec![(x, y - 1)],
        _ => vec![], // No valid moves for other characters
    }
}

fn steps_down(grid: &Vec<Vec<char>>, pos: Pos) -> Vec<(Pos)> {
    let (x, y) = pos;
    match grid[y][x] {
        '┏' => vec![(x, y + 1)],
        '┓' => vec![(x, y + 1)],
        '┛' => vec![(x - 1, y)],
        '┗' => vec![(x + 1, y)],
        '┣' => vec![(x, y + 1), (x + 1, y)],
        '┫' => vec![(x - 1, y), (x, y + 1)],
        '┻' => vec![(x - 1, y), (x + 1, y)],
        '╋' => vec![(x - 1, y), (x, y + 1), (x + 1, y)],
        '┳' => vec![(x - 1, y), (x + 1, y), (x, y + 1)],
        '━' => vec![(x - 1, y), (x + 1, y)],
        '┃' => vec![(x, y + 1)],
        _ => vec![], // No valid moves for other characters
    }
}

fn find_tokens(data: &str, row: usize) -> Result<Vec<Token>, ParseError> {
    let mut tokens = Vec::new();
    let re = regex::Regex::new(r"[ ━┃┓┏┛┗┣┫┳┻╋][:\w\-\+\*(<=)]+[ ━┃┓┏┛┗┣┫┳┻╋]")?;
    for mat in re.find_iter(data) {
        let mut token_str: Vec<char> = mat.as_str().chars().skip(1).collect();
        token_str.pop();
        let token_str: String = token_str.into_iter().collect();

        let start_col = data[..mat.start()].chars().count() + 1 + 1;
        let end_col = start_col + token_str.chars().count() - 1;
        tokens.push(Token {
            name: token_str.clone(),
            position: Position {
                bottom_left: (start_col, row),
                top_right: (end_col, row),
            },
        });
    }
    Ok(tokens)
}

fn parse_box_tops(
    data: &str,
    row: usize,
    char_grid: &Vec<Vec<char>>,
) -> Result<Vec<Box>, ParseError> {
    let mut result = Vec::new();
    let box_top_re = regex::Regex::new(r"┏━*\{(?P<token>[:\w\-]+)\}━*┓")?;
    //TODO: These are only potential boxes. Need to confirm they go all the way around. This could just be a fn with 2 outputs
    for mat in box_top_re.find_iter(data) {
        let start = data[..mat.start()].chars().count() + 1;
        let end = start + mat.as_str().chars().count() - 1;
        let caps = box_top_re
            .captures(data)
            .ok_or_else(|| ParseError::Other("Failed to capture box top".to_string()))?;
        let token = caps
            .name("token")
            .map(|m| m.as_str())
            .ok_or_else(|| ParseError::Other("No token in box top".to_string()))?;

        let col = start;
        // Use while let for a cleaner loop
        let mut current_row = row + 1;
        while current_row < char_grid.len() {
            let ch = char_grid[current_row][col];
            match ch {
                '┃' => current_row += 1,
                '┗' => break,
                _ => {
                    return Err(ParseError::UnexpectedBoxChar {
                        ch,
                        col,
                        row: current_row,
                    });
                }
            }
        }
        if current_row >= char_grid.len() {
            return Err(ParseError::BoxVerticalLineExceededGridBounds);
        }

        result.push(Box {
            name: token.to_string(),
            position: Position {
                bottom_left: (col, current_row),
                top_right: (end, row),
            },
        });
    }
    Ok(result)
}

fn print(boxes: &[Box], tokens: &[Token]) {
    let width = tokens.iter().map(|t| t.name.len()).max().unwrap_or(0);

    for b in boxes {
        log!(
            "Box: {:width$} | Position: bottom_left: {:?}, top_right: {:?}",
            b.name,
            b.position.bottom_left,
            b.position.top_right
        );
    }

    for (i, token) in tokens.iter().enumerate() {
        let nums_width = (tokens.len() as u32).ilog10() as usize + 1;
        log!(
            "Token[{:nums_width$}]: {:width$} | Position: bottom_left: {:?}, top_right: {:?}",
            i,
            token.name,
            token.position.bottom_left,
            token.position.top_right
        );
    }
}

fn print_edges(edges: &Vec<Vec<(NodeIndex, OutputIndex)>>, tokens: &[Token]) {
    log!("");
    for (i, edge) in edges.iter().enumerate() {
        let token_name = &tokens[i].name;
        let edge_str = edge
            .iter()
            .map(|(node, output)| format!("{}[{}]", tokens.get(node.0).unwrap().name, output.0))
            .collect::<Vec<_>>()
            .join(", ");
        log!("Edges for token '{}': {}", token_name, edge_str);
    }
}

#[derive(Debug)]
pub struct Token {
    pub name: String,
    pub position: Position,
}

#[derive(Debug)]
pub struct Box {
    pub name: String,
    pub position: Position,
}

#[derive(Debug)]
pub struct Position {
    pub bottom_left: Pos,
    pub top_right: Pos,
}

static SYMBOLS: &[&str] = &["━", "┃", "┓", "┏", "┛", "┗", "┣", "┫", "┳", "┻", "╋"];
// ━┃┓┏┛┗┣┫┳┻╋
static ABOVE: &[&str] = &["┃", "┏", "┓", "┳", "╋"];
static LEFT: &[&str] = &["━", "┗", "┣", "┳", "┻", "╋"];
static RIGHT: &[&str] = &["━", "┛", "┫", "┳", "┻", "╋"];

// Shouldn't need these
// static BELOW: &[&str] = &["┃", "┗", "┛", "┻", "╋"];
// static CORNERS: &[&str] = &["┏", "┓", "┗", "┛"];

fn create_grid(lines: &[&str]) -> Vec<Vec<char>> {
    let max_width = lines
        .iter()
        .map(|line| line.chars().count() + 1)
        .max()
        .unwrap_or(0);
    let mut grid: Vec<Vec<char>> = lines
        .iter()
        .map(|line| {
            let mut chars: Vec<char> = line.chars().collect();
            chars.insert(0, ' ');
            chars.resize(max_width, ' ');
            chars
        })
        .collect();
    grid.insert(0, vec![' '; max_width]);
    grid
}

fn token_to_node(t: &Token, tokens: &[Token], box_num: usize) -> Node {
    if let Ok(val) = t.name.parse() {
        return Node::Value(Value::Int(val));
    }
    if BUILTIN_FNS.contains(&t.name.as_str()) || SPECIAL_BUILTIN_FNS.contains(&t.name.as_str()) {
        return Node::BuiltIn(t.name.clone());
    }
    if t.name.starts_with(':') {
        return if let Ok(arg_order) = t.name.strip_prefix(":").unwrap().parse::<usize>() {
            Node::Arg(ArgOrder(arg_order - 1))
        } else {
            Node::Defn
        };
    }
    let target_name = ":".to_string() + &t.name;
    let i = tokens.iter().position(|x| x.name == target_name).unwrap();
    Node::FnCall(ScopeIdx(box_num as usize), NodeIndex(i))
}
