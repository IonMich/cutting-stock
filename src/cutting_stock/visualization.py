"""Visualization utilities for cutting stock patterns."""

import numpy as np
from typing import List, Optional


def create_stock_visualization(lengths: List[float], pattern: np.ndarray, roll_length: float, max_decimal_places: int = 1, indent: str = "          ") -> str:
    """Create ASCII art visualization of a cutting pattern with aligned length labels."""
    # Calculate the visual representation
    visual_parts = []
    label_parts = []
    current_pos = 0.0  # Use float to match length types
    colors = ['█', '▓', '▒', '░', '▆', '▅', '▄', '▃']  # Different patterns for different lengths
    
    # Create segments for each piece type
    for j, length in enumerate(lengths):
        count = int(pattern[j])
        if count > 0:
            # Use different characters for different piece lengths
            char = colors[j % len(colors)]
            segment_length = int((length * 20) / roll_length)  # Scale to ~20 chars max
            segment_length = max(3, segment_length)  # At least 3 chars to fit labels
            
            for _ in range(count):
                visual_parts.append(char * segment_length)
                # Create label for this piece
                label = f'{length}m'
                # Center the label over the segment, accounting for exact segment length
                if len(label) >= segment_length:
                    # If label is too long, truncate or abbreviate
                    if segment_length >= 4:
                        label = f'{length:.1f}m'[:segment_length]
                    else:
                        label = str(length)[:segment_length]
                
                padding = segment_length - len(label)
                left_pad = padding // 2
                right_pad = padding - left_pad
                centered_label = ' ' * left_pad + label + ' ' * right_pad
                label_parts.append(centered_label)
                current_pos += length
    
    # Handle waste
    waste = roll_length - current_pos
    waste_segment = ""
    waste_label = ""
    if waste > 0:
        waste_length = int((waste * 20) / roll_length)
        # Ensure minimum width to fit decimal waste values like "1.8m"
        waste_length = max(4, waste_length)
        waste_segment = '·' * waste_length
        # Add waste label using the correct decimal places
        waste_text = f'{waste:.{max_decimal_places}f}m'
        # Only truncate if absolutely necessary, but prefer keeping precision
        if len(waste_text) > waste_length:
            if max_decimal_places > 0:
                # Try reducing decimal places before giving up
                waste_text = f'{waste:.0f}m'
            if len(waste_text) > waste_length:
                waste_text = '···'[:waste_length]
        
        padding = waste_length - len(waste_text)
        left_pad = padding // 2
        right_pad = padding - left_pad
        waste_label = ' ' * left_pad + waste_text + ' ' * right_pad
    
    # Join pieces with cut separators - labels and visual must align
    visual = '|'.join(visual_parts)
    labels = '|'.join(label_parts)
    
    if waste_segment:
        if visual:  # Add separator before waste if there are pieces
            visual += '|'
            labels += '|'
        visual += waste_segment
        labels += waste_label
    
    # Ensure total length doesn't exceed display width
    if len(visual) > 40:
        visual = visual[:37] + '...'
        labels = labels[:37] + '...'
    
    # Create the two-line output with proper alignment
    result = f'{labels}\n{indent}{visual} ({roll_length}m stock)'
    
    return result


def create_input_visualization(lengths: List[float], quantities: List[int], max_decimal_places: int = 1) -> str:
    """Create ASCII art visualization showing the required pieces on a single line."""
    colors = ['█', '▓', '▒', '░', '▆', '▅', '▄', '▃']  # Same colors as cutting patterns
    
    pieces = []
    for i, (length, qty) in enumerate(zip(lengths, quantities)):
        char = colors[i % len(colors)]
        # Create visual with proper spacing: "███ 3.4m ×34"
        pieces.append(f'{char * 3} {length}m ×{qty}')
    
    # Join all pieces on a single line with separators
    return '   '.join(pieces)


def display_concise_output(lengths: np.ndarray, q: np.ndarray, roll_length: float, 
                          x_value: np.ndarray, objective_value: float, A: np.ndarray, 
                          c: List[float], max_decimal_places: int) -> None:
    """Display concise output with input summary and pattern visualizations."""
    # Show complete input specification
    input_viz = create_input_visualization(lengths.tolist(), [int(qty) for qty in q], max_decimal_places)
    print('Required pieces:')
    print(input_viz)
    print(f'Stock length: {roll_length}m')
    print()
    
    # Show solution summary
    total_stocks = int(round(sum(x_value)))
    print(f'Solution: {total_stocks} stocks of {roll_length}m each, {objective_value:.1f}m waste')
    print()
    
    # Show cutting patterns
    for i in range(len(c)):
        if x_value[i] > 0:
            times_used = int(round(float(x_value[i])))
            # Use consistent width for the prefix to maintain alignment
            prefix = f'Use {times_used:2}× → '
            print(prefix + create_stock_visualization(lengths.tolist(), A[:, i], roll_length, max_decimal_places))


def display_verbose_output(lengths: np.ndarray, q: np.ndarray, roll_length: float, 
                          x_value: np.ndarray, objective_value: float, A: np.ndarray, 
                          c: List[float], max_decimal_places: int) -> None:
    """Display detailed verbose output with full specifications and analysis."""
    total_material_needed = lengths @ q
    theoretical_minimum = np.ceil(total_material_needed / roll_length)
    
    print('CUTTING STOCK OPTIMIZATION RESULTS')
    print('=' * 50)
    print()
    
    print('INPUT SPECIFICATIONS:')
    print(f'• Stock length: {roll_length} m')
    print(f'• Total material needed: {total_material_needed:.1f} m')
    print('• Required pieces:')
    input_viz = create_input_visualization(lengths.tolist(), [int(qty) for qty in q], max_decimal_places)
    # Indent the input visualization
    indented_viz = '\n'.join('  ' + line for line in input_viz.split('\n'))
    print(indented_viz)
    print()

    total_stocks = int(round(sum(x_value)))
    waste_rate = (objective_value / (total_stocks * roll_length)) * 100
    
    print('OPTIMIZATION SUMMARY:')
    print('• Status: Optimal solution found')
    print(f'• Stocks used: {total_stocks} pieces')
    print(f'• Total waste: {objective_value:.1f} m ({waste_rate:.1f}% waste rate)')
    print(f'• Theoretical minimum: {int(theoretical_minimum)} stocks')
    print()
    
    print('CUTTING PATTERNS:')
    print('=' * 20)
    
    # Create legend for ASCII art
    print('Legend:')
    colors = ['█', '▓', '▒', '░', '▆', '▅', '▄', '▃']
    legend_parts = []
    for j, length in enumerate(lengths):
        char = colors[j % len(colors)]
        legend_parts.append(f'{char} = {length}m')
    print(f'  {" ".join(legend_parts)}   · = waste   | = cuts')
    print()
    
    pattern_num = 1
    for i in range(len(c)):
        if x_value[i] > 0:
            times_used = int(round(float(x_value[i])))
            waste_per_stock = c[i]
            total_waste = waste_per_stock * times_used
            
            print(f'Pattern #{pattern_num}: Use {times_used} stock{"s" if times_used > 1 else ""}')
            
            # Build cut description
            cuts = []
            for j in range(len(q)):
                if A[j][i] > 0:
                    cuts.append(f'{A[j][i]} piece{"s" if A[j][i] > 1 else ""} of {lengths[j]}m')
            
            if cuts:
                print(f'• Cut: {" + ".join(cuts)}')
            print(f'• Waste per stock: {waste_per_stock:.1f}m')
            print(f'• Total waste: {total_waste:.1f}m')
            
            # ASCII art visualization
            print('• Visual:')
            visualization = create_stock_visualization(lengths.tolist(), A[:, i], roll_length, max_decimal_places, indent="  ")
            print('  ' + visualization)
            print()
            
            pattern_num += 1


def display_output(lengths: np.ndarray, q: np.ndarray, roll_length: float, 
                  status: str, x_value: Optional[np.ndarray], objective_value: Optional[float], 
                  A: np.ndarray, c: List[float], max_decimal_places: int, verbose: bool = False) -> None:
    """Display output based on optimization results and verbosity level."""
    if status == 'optimal' and x_value is not None and objective_value is not None:
        if verbose:
            display_verbose_output(lengths, q, roll_length, x_value, objective_value, A, c, max_decimal_places)
        else:
            display_concise_output(lengths, q, roll_length, x_value, objective_value, A, c, max_decimal_places)
    else:
        print(f'Status: {status}')
        if objective_value is not None:
            print(f'Total waste: {objective_value:.1f} m')