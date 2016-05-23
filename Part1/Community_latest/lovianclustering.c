#include <stdio.h>
#include <stdlib.h>
#include <string.h>
FILE *fp;
int main(){
	//printf("Hello World");
	char *line = NULL;
    size_t len = 0;
    ssize_t read;
    char *filename = "./graphs/";

    


	fp = fopen("filelist.txt", "r");
	if (fp == NULL)
        exit(EXIT_FAILURE);
    while ((read = getline(&line, &len, fp)) != -1) {
        //printf("Retrieved line of length %zu :\n", read);
    	char *file = (char *) malloc(1 + strlen(filename)+ strlen(line) );
      	strcpy(file, filename);
      	strcat(file, line);
        char command[200];
        memset(command, 0, 199);
        strcpy(command, "./convert -i ");
        strcat(command, file);
        command[strlen(command) - 1] = ' ';
        strcat(command, " -o graph.bin -w graph.weights");
        printf("%s\n", command);
        system(command);
        memset(command, 0, 199);
        system("./community graph.bin -l -1 -w graph.weights > graph.tree");
        system("./hierarchy graph.tree");

        char resCommand[200];
        memset(resCommand, 0, 199);
        strcat(resCommand, "./hierarchy graph.tree -l 1 > ");
        strcat(resCommand, "./clusteredGraphs/");
        strcat(resCommand, line);
        system(resCommand);
        memset(command, 0, 199);
    }
	return 0;
}