import java.io.*;
import java.util.*;

/** BFS solution. Input: T, N, then N rows (characters or space-separated cells). */
public class MazeKeys {
    static class State {
        int r, c, mask, dist;
        State(int r, int c, int mask, int dist) { this.r=r; this.c=c; this.mask=mask; this.dist=dist; }
    }
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        ArrayList<String> lines = new ArrayList<>(); String line;
        while ((line=br.readLine()) != null) if (!line.trim().isEmpty()) lines.add(line.trim());
        if (lines.size() < 2) throw new IllegalArgumentException("Expected T, N, and N grid rows.");
        int t = Integer.parseInt(lines.get(0));
        int n = Integer.parseInt(lines.get(1));
        if (t < 1 || t > 6 || lines.size() < n+2) throw new IllegalArgumentException("Invalid T, N, or missing rows.");
        char[][] g = new char[n][n]; int sr=-1, sc=-1, exits=0;
        for (int r=0; r<n; r++) {
            String row = lines.get(r+2).replaceAll("[,\\s]", "");
            if (row.length()!=n) throw new IllegalArgumentException("Grid must be square.");
            for (int c=0;c<n;c++) {
                char x=row.charAt(c); g[r][c]=x;
                if (x=='S') { if(sr!=-1) throw new IllegalArgumentException("Multiple starts."); sr=r; sc=c; }
                else if(x=='E') exits++;
                else if(".#abcdefABCDEF".indexOf(x)<0) throw new IllegalArgumentException("Invalid grid character: "+x);
            }
        }
        if(sr<0 || exits!=1) throw new IllegalArgumentException("Need exactly one S and E.");
        boolean[] keys=new boolean[6], doors=new boolean[6];
        for(char[] row:g) for(char x:row) { if(x>='a'&&x<='f') keys[x-'a']=true; if(x>='A'&&x<='F') doors[x-'A']=true; }
        int types=0; for(int i=0;i<6;i++) { if(keys[i]!=doors[i]) throw new IllegalArgumentException("Key/door types must be paired."); if(keys[i]) types++; }
        if(types!=t) throw new IllegalArgumentException("T does not match grid.");
        boolean[][][] seen=new boolean[n][n][64]; ArrayDeque<State> q=new ArrayDeque<>();
        q.add(new State(sr,sc,0,0)); seen[sr][sc][0]=true;
        int[] dr={-1,1,0,0}, dc={0,0,-1,1}; int ans=-1;
        while(!q.isEmpty()) {
            State s=q.remove();
            if(g[s.r][s.c]=='E') { ans=s.dist; break; }
            for(int k=0;k<4;k++) {
                int r=s.r+dr[k], c=s.c+dc[k]; if(r<0||r>=n||c<0||c>=n||g[r][c]=='#') continue;
                char x=g[r][c]; if(x>='A'&&x<='F'&&(s.mask&(1<<(x-'A')))==0) continue;
                int m=s.mask; if(x>='a'&&x<='f') m|=1<<(x-'a');
                if(!seen[r][c][m]) { seen[r][c][m]=true; q.add(new State(r,c,m,s.dist+1)); }
            }
        }
        System.out.println(ans);
    }
}
