#include <stdio.h>
#include <limits.h>
int minPathValue(int n, int array[][n], int kx, int ky,
	int tx, int ty) {
	printf("%d %d\n", kx, ky);
	if (kx == tx && ky == ty) {
		array[tx][ty] = 0;
		return 0;
	} else {
		if (array[kx][ky] == 1) {
			printf("Already exploring %d %d\n", kx, ky);
			return INT_MAX;
		}
		array[kx][ky] = 1;
		int min = INT_MAX;
		if (kx-2>=0 && ky-1>=0) {
			int min1 = minPathValue(n,array,kx-2,ky-1,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx-2,ky-1,min1);
			min = min1<min?min1:min;
		}
		if (kx-2>=0 && ky+1<n) {
			int min1 = minPathValue(n,array,kx-2,ky+1,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx-2,ky+1,min1);
			min = min1<min?min1:min;
		}
		if (kx-1>=0 && ky-2>=0) {
			int min1 = minPathValue(n,array,kx-1,ky-2,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx-1,ky-2,min1);
			min = min1<min?min1:min;
		}
		if (kx-1>=0 && ky+2<n) {
			int min1 = minPathValue(n,array,kx-1,ky+2,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx-1,ky+2,min1);
			min = min1<min?min1:min;
		}
		if (kx+1<n && ky-2>=0) {
			int min1 = minPathValue(n,array,kx+1,ky-2,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx+1,ky-2,min1);
			min = min1<min?min1:min;
		}
		if (kx+1<n && ky+2<n) {
			int min1 = minPathValue(n,array,kx+1,ky+2,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx+1,ky+2,min1);
			min = min1<min?min1:min;
		}
		if (kx+2<n&&ky-1>=0) {
			int min1 = minPathValue(n,array,kx+2,ky-1,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx+2,ky-1,min1);
			min = min1<min?min1:min;
		}
		if (kx+2<n&&ky+1<n) {
			int min1 = minPathValue(n,array,kx+2,ky+1,tx,ty);
			printf("%d %d --> %d %d: min: %d\n", kx, ky, kx+2,ky+1,min1);
			min = min1<min?min1:min;
		}
		array[kx][ky] = -1;
		if (min == INT_MAX) {
			return min;
		} else {
			printf("%d %d Returning %d \n", kx, ky,min+1);
			return min+1;
		}
	}
}
void printArray(int n, int array[][n]) {
	int i = 0;
	int j = 0;
	for (i = 0; i < n; i++) {
		for (j = 0; j < n; j++) {
			printf("%d ", array[i][j]);
		}
		printf("\n");
	}
}
int main() {
	int numTests = 0;
	int i = 0;
	scanf("%d", &numTests);
	for (i = 0; i < numTests; i++) {
		int n = 0;
		scanf("%d", &n);
		int array[n][n];
		int j = 0;
		int k = 0;
		for (j = 0; j < n; j++) {
			for (k = 0; k < n; k++) {
				array[j][k] = -1;
			}
		}
		int kx, ky = 0;
		scanf("%d %d", &kx, &ky);
		int tx, ty = 0;
		scanf("%d %d", &tx, &ty);
		int min = minPathValue(n, array, kx-1, ky-1, tx-1, ty-1);
		printArray(n, array);
		printf("%d\n", min);
	}
	return 0;
}
