import java.util.LinkedList;
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
		public NodeLevel(Node node, int level){
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
				if (cur.left == null){
					cur.left = new Node(data);
					return true;
				}
				cur = cur.left;
			}
		}
		return false;
	}
	
	public void printTreeLevel(){
		if (root == null)
			return;
		int curLevel = 0;
		LinkedList<NodeLevel> nodeList = new LinkedList<>();
		nodeList.offer(new NodeLevel(root, 0));
		while(true){
			NodeLevel nl = nodeList.poll();
			if (nl == null)
				break;
			if (nl.level != curLevel){
				System.out.println("\n");
				curLevel = nl.level;
			}
			System.out.print(nl.node.value + " ");
			if (nl.node.left != null){
				nodeList.offer(new NodeLevel(nl.node.left, nl.level + 1));
			}
			if (nl.node.right != null){
				nodeList.offer(new NodeLevel(nl.node.right, nl.level + 1));
			}
		}
		
	}
}
