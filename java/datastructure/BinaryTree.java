import java.util.LinkedList;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public class BinaryTree {
	private static class Node {
		int value;
		Node left;
		Node right;

		public Node(int value) {
			this.value = value;
			this.left = this.right = null;
		}
	}

	private static class NodeLevel {
		Node node;
		int level;

		public NodeLevel(Node node, int level) {
			this.node = node;
			this.level = level;
		}
	}

	private Node root;
	public BinaryTree() {
		root = null;
	}

	public boolean insert(int data) {
		if (root == null) {
			root = new Node(data);
			return true;
		}
		Node cur = root;
		while (cur != null) {
			if (cur.value == data) {
				break;
			} else if (cur.value < data) {
				if (cur.right == null) {
					cur.right = new Node(data);
					return true;
				}
				cur = cur.right;
			} else {
				if (cur.left == null) {
					cur.left = new Node(data);
					return true;
				}
				cur = cur.left;
			}
		}
		return false;
	}

	public boolean lookup(int data) {
		Node cur = root;
		while (cur != null) {
			if (cur.value == data)
				return true;
			if (cur.value > data)
				cur = cur.right;
			else
				cur = cur.left;
		}
		return false;
	}

	private int size(Node node) {
		if (node == null)
			return 0;
		int theSize = 1;
		if (node.left != null)
			theSize += size(node.left);
		if (node.right != null)
			theSize += size(node.right);
		return theSize;
	}

	public int size() {
		return size(root);
	}

	private int maxDepth(Node node) {
		if (node == null)
			return 0;
		return 1 + Math.max(maxDepth(node.right), maxDepth(node.left));
	}

	public int maxDepth() {
		return maxDepth(root);
	}

	public void printTreeLevel() {
		if (root == null)
			return;
		int curLevel = 0;
		LinkedList<NodeLevel> nodeList = new LinkedList<>();
		nodeList.offer(new NodeLevel(root, 0));
		while (true) {
			NodeLevel nl = nodeList.poll();
			if (nl == null)
				break;
			if (nl.level != curLevel) {
				System.out.println("\n");
				curLevel = nl.level;
			}
			System.out.print(nl.node.value + " ");
			if (nl.node.left != null) {
				nodeList.offer(new NodeLevel(nl.node.left, nl.level + 1));
			}
			if (nl.node.right != null) {
				nodeList.offer(new NodeLevel(nl.node.right, nl.level + 1));
			}
		}

	}

	int maxValue() throws Exception {
		if (root == null)
			throw new Exception("Empty");
		Node cur = root;
		while (true) {
			if (cur.right == null)
				return cur.value;
			cur = cur.right;
		}
	}

	int minValue() throws Exception {
		if (root == null)
			throw new Exception("Empty");
		Node cur = root;
		while (true) {
			if (cur.left == null)
				return cur.value;
			cur = cur.left;
		}
	}
	
	/**
	 *  Returns the total number of unique binary search trees with 
	 *  n tree nodes
	 */
	public static int countUniqueTrees(int n){
		if (n <= 1)
			return 1;
		int root = 1, left, right;
		int sum = 0;
		while(root <= n){
			left = countUniqueTrees(root - 1);
			right = countUniqueTrees(n - root);
			sum += left * right;
			root++;
		}
		return sum;
	}

	/**
	 * 
	 * @param tree
	 * @return true if the tree is a proper binary tree
	 */
	public static boolean isBinaryTree(BinaryTree tree){
		Node node = tree.root;
		return isBianryTree(node);
	}
	
	private static boolean isBianryTree(Node node){
		if (node == null)
			return true;
		if (node.left != null && node.left.value > node.value){
			return false;
		}
		if (node.right != null && node.right.value <= node.value){
			return false;
		}
		
		return (node.right == null || isBianryTree(node.right))
				&& (node.left == null || isBianryTree(node.left));
	}
	
	
	/**
	 * 
	 * @param sum
	 * @return checks if any of the path has the given sum
	 */
	public boolean hasPathSum(int sum){
		return hasPathSum(sum, root);
	}
	
	private boolean hasPathSum(int sum, Node node){
		if (node == null)
			return sum == 0;
		if (node.left == null && node.right == null)
			return ((sum - node.value) == 0);
	
		int remainsum = sum - node.value;
		if (sum <= 0)
			return false;
		Node temp = node.left;
		if (temp != null && hasPathSum(remainsum, temp))
			return true;
		temp = node.right;
		if (temp != null && hasPathSum(remainsum, temp))
			return true;
		return false;
			
	}
	
	/**
	 * This routines print all the paths in the tree
	 */
	public void printPaths(){
		if (root == null)
			return;
		LinkedList<Node> nl = new LinkedList<>();
		printPaths(root,nl);
	}
	
	private void printPaths(Node node, LinkedList<Node> nl){
		if (node.left == null && node.right == null){
			System.out.print("Path= ");
			for (Node n : nl){
				System.out.print(n.value + " ");
			}
			System.out.println(node.value);
			return;
		} 
		nl.add(node);
		if (node.right != null){
			printPaths(node.right, nl);
		}
		if (node.left != null){
			printPaths(node.left, nl);
		}
		nl.removeLast();
	}
	
	private void mirror(Node node){
		Node left = node.left;
		left = node.right;
		node.right = left;
		if (node.right != null)
			mirror(node.right);
		if (node.left != null)
			mirror(node.left);
	}
	
	public void mirror(){
		if (root == null)
			return;
		mirror(root);
	}
	
	private void doubleTree(Node node){
		if (node == null)
			return;
		if (node.left != null){
			Node newleft = new Node(node.left.value);
			newleft.right = null;
			newleft.left = node.left;
			node.left = newleft;
			doubleTree(newleft.left);
		}
		doubleTree(node.right);
			
	}
	
	public void doubleTree(){
		if (root == null)
			return;
		doubleTree(root);
	}
	
	public static void main(String[] args) {
		BinaryTree bn = new BinaryTree();
		Random r = new Random();
		Set<Integer> ints = new TreeSet<>();
		int i = 0;
		int j = 0;
		while (i < 5) {
			j = r.nextInt(1000000);
			if (ints.contains(j)) {
				continue;
			}
			ints.add(j);
			bn.insert(j);
			i++;
		}
		System.out.println(bn.size());
		bn.printPaths();
		try {
			System.out.println("Min " + bn.minValue());
			System.out.println("Max " + bn.maxValue());
		} catch (Exception e) {

		}
		bn = new BinaryTree();
		bn.insert(5);
		bn.insert(2);
		bn.insert(7);
		bn.insert(9);
		System.err.println(bn.maxDepth());
		System.err.println("Unique trees " + BinaryTree.countUniqueTrees(3));
	}
}
