from collections import Counter, defaultdict
import heapq
import math
from flask import Blueprint, render_template, request
from forms import TextForm
import sys
import json  # Import the json module

text_bp = Blueprint('text', __name__)

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq
    def to_dict(self):
        return {
            'char': self.char,
            'freq': self.freq,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
        

class CompressionAnalyzer:
    def calculate_entropy(self, text):
        freq = Counter(text)
        length = len(text)
        entropy = -sum((count/length) * math.log2(count/length) for count in freq.values())
        return entropy
    
    def analyze_distribution(self, text):
        counts = Counter(text)
        unique_chars = len(counts)
        max_freq = max(counts.values())
        return {
            'unique_chars': unique_chars,
            'max_freq': max_freq,
            'distribution_score': max_freq / len(text)
        }

    def select_algorithm(self, text):
        entropy = self.calculate_entropy(text)
        distribution = self.analyze_distribution(text)
        
        if entropy < 3 and distribution['distribution_score'] > 0.3:
            return 'rle'
        elif distribution['unique_chars'] < 64:
            return 'huffman'
        else:
            return 'arithmetic'

class TextCompressor:
    def rle_compress(self, text):
        compressed = []
        count = 1
        current = text[0]
        
        for char in text[1:]:
            if char == current:
                count += 1
            else:
                compressed.append(f"{count}{current}")
                current = char
                count = 1
                
        compressed.append(f"{count}{current}")
        return "".join(compressed)
    
    def rle_decompress(self, compressed):
        decompressed = []
        i = 0
        while i < len(compressed):
            count = ""
            while i < len(compressed) and compressed[i].isdigit():
                count += compressed[i]
                i += 1
            if i < len(compressed):
                decompressed.append(compressed[i] * int(count))
                i += 1
        return "".join(decompressed)

    def huffman_compress(self, text):
        freq = Counter(text)
        heap = [Node(char, count) for char, count in freq.items()]
        heapq.heapify(heap)
        
        codes = {}
        tree = None
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            internal = Node(None, left.freq + right.freq)
            internal.left = left
            internal.right = right
            
            heapq.heappush(heap, internal)
            tree = internal
            
        def generate_codes(node, code=""):
            if node.char:
                codes[node.char] = code
                return
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")
            
        generate_codes(tree)
        compressed = "".join(codes[char] for char in text)
        return compressed, codes, tree
    
    def huffman_decompress(self, compressed, tree):
        decompressed = []
        current = tree
        
        for bit in compressed:
            if bit == "0":
                current = current.left
            else:
                current = current.right
                
            if current.char:
                decompressed.append(current.char)
                current = tree
                
        return "".join(decompressed)

    def arithmetic_compress(self, text):
        freq = Counter(text)
        prob = {char: count/len(text) for char, count in freq.items()}
        
        low = 0.0
        high = 1.0
        range_size = 1.0
        
        for char in text:
            range_size = high - low
            high = low + range_size * sum(prob[c] for c in prob if c <= char)
            low = low + range_size * sum(prob[c] for c in prob if c < char)
            
        return (low + high)/2, prob
    
    def arithmetic_decompress(self, value, prob, length):
        ranges = {}
        current = 0
        for char in sorted(prob):
            ranges[char] = (current, current + prob[char])
            current += prob[char]
            
        result = []
        current_value = value
        
        for _ in range(length):
            for char, (low, high) in ranges.items():
                if low <= current_value < high:
                    result.append(char)
                    current_value = (current_value - low)/(high - low)
                    break
                    
        return "".join(result)

    def get_huffman_tree_json(self, tree):
        """Converts the Huffman tree to a JSON serializable dictionary."""
        if tree:
            return json.dumps(tree.to_dict())
        return None

@text_bp.route('/text', methods=['GET', 'POST'])
def text():
    form = TextForm()
    if form.validate_on_submit():
        text_data = form.text_data.data
        
        analyzer = CompressionAnalyzer()
        compressor = TextCompressor()
        
        algorithm = analyzer.select_algorithm(text_data)
        result = {}
        
        if algorithm == 'rle':
            compressed = compressor.rle_compress(text_data)
            decompressed = compressor.rle_decompress(compressed)
            result = {
                'algorithm': 'RLE',
                'compressed': compressed,
                'decompressed': decompressed,
                'compression_ratio': len(compressed)/len(text_data)
            }
        
        elif algorithm == 'huffman':
            compressed, codes, tree = compressor.huffman_compress(text_data)
            decompressed = compressor.huffman_decompress(compressed, tree)
            tree_json = compressor.get_huffman_tree_json(tree)
            result = {
                'algorithm': 'Huffman',
                'compressed': compressed,
                'decompressed': decompressed,
                'codes': codes,
                'compression_ratio': len(compressed)/(len(text_data) * 8),
                'tree_json': tree_json            }
            
        else:  # arithmetic
            compressed, prob = compressor.arithmetic_compress(text_data)
            decompressed = compressor.arithmetic_decompress(compressed, prob, len(text_data))
            result = {
                'algorithm': 'Arithmetic',
                'compressed': compressed,
                'decompressed': decompressed,
                'compression_ratio': sys.getsizeof(compressed)/sys.getsizeof(text_data)
            }
            
        return render_template('text.html', form=form, result=result)
    
    return render_template('text.html', form=form)