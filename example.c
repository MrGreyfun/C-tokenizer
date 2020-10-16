#include <stdio.h>
#include <stdlib.h>
/*
implement the "input" function, which can get one line from system's standard input stream
*/

struct CharNode
{
	char c;
	struct CharNode* next;
};


char* input()
{
	char inputChar = getchar();
	int count = 0;
	struct CharNode* node = (struct CharNode*)malloc(sizeof(struct CharNode));
	struct CharNode* head = node;
	while (inputChar != '\n')
	{
		node->c = inputChar;
		node->next = (struct CharNode*)malloc(sizeof(struct CharNode));
		node = node->next;
		count++;
		inputChar = getchar();
	}
	node->next = NULL;
	//convert linked list into String(char array)
	char* inputString = (char*)malloc(sizeof(char) * (count+1));
	node = head;
	for (int i = 0; i < count; i++)
	{
		inputString[i] = node->c;
		node = node->next;
	}
	inputString[count] = '\0';
	return inputString;

}

int main()
{
	char* inputString = input();
	printf("%s", inputString);
	return 0;
}