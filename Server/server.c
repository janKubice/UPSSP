/**
 * Server pro hru
 * prelozi se prikazem gcc server.c -lpthread -o server
 * 
 * Author: Jan Kubice
 * Date: 27.12.2021
 * Version: Fakt obri cislo
 */ 

#include<stdio.h>
#include<string.h>    
#include<stdlib.h>    
#include<sys/socket.h>
#include<arpa/inet.h> 
#include<unistd.h> 
#include<pthread.h>

#define CLIENT_MSG_SIZE 512

#define REQ_ID "1"
#define CONNECT_TO_GAME "2"
#define RECONNECT_TO_GAME "3"
#define CREATE_NEW_ROOM "4"
#define START_GAME "5"
#define SEND_QUIZ_ANSWER "6"
#define PAUSE_GAME "7"
#define LEAVE_GAME "8"
#define NEXT_QUESTION "9"


#define STATE_IN_LOBBY 1
#define STATE_IN_GAME 2
#define STATE_IN_PAUSE 3
#define STATE_ENDED 4

#define OK "100"
#define ERR "-1"
#define NUMBER_OF_PLAYERS 90
#define NUMBER_OF_ROOMS 30
#define NUMBER_OF_QUESTIONS 2


void *connection_handler(void *);


typedef struct Player
{
    //id hráče
    int id_p; 
    // počet bodů
    int points;
    //socket = abych věděla kam posílat zprávy
    int socket;
} player;

typedef struct Game
{
    //id místnosti
    int id_r;

    int availability[3];
    //pole hráčů
    player array_p[3];
    //stav hry
    int state;
    //počet hráčů ve hře
    int number_players;
    int q_ids[2];
    //v jakém kole je hra
    int round;

} game;

typedef struct Question
{
    char *question;
    char *ans1;
    char *ans2;
    char *ans3;
    char *ans4;
    int correct;

} question;

player* players = NULL;
game* games = NULL;
question* questions = NULL;

/**
 * @brief Vstupni bod programu
 * 
 * @param argc pocet argumentu
 * @param argv pole argumentu
 * @return int navratova hodnota programu
 */
int main(int argc , char *argv[])
{
    players = calloc(NUMBER_OF_PLAYERS,sizeof(player));
    games = calloc(NUMBER_OF_ROOMS, sizeof(game));

    questions = calloc(NUMBER_OF_QUESTIONS, sizeof(question));

    questions[0].question = "Jakou barvu má sluníčko";
    questions[0].ans1 = "modrá";
    questions[0].ans2 = "žlutá";
    questions[0].ans3 = "černá";
    questions[0].ans4 = "růžová";
    questions[0].correct = 2;

    questions[1].question = "Kdo je nejlepší cvičící na UPS";
    questions[1].ans1 = "Skupa";
    questions[1].ans2 = "Pepa";
    questions[1].ans3 = "Adam";
    questions[1].ans4 = "Bořek";
    questions[1].correct = 1;

    int i;
    for(i = 0; i < NUMBER_OF_PLAYERS; i++){
        players[i].id_p=-1;
    }


    int h;
    for(i = 0; i < NUMBER_OF_ROOMS; i++){
        int pole[2] = {0,1}; //TODO tady pole generovat
        games[i].id_r = -1;
        games[i].round = 0;
        memcpy(games[i].q_ids, pole , sizeof(games[i].q_ids));
        for (h = 0;h < 3; h++){
            games[i].availability[h] = 0;
        }
    }

    
    int socket_desc , client_sock , c;
    struct sockaddr_in server , client;
     
    //vytvoreni socketu
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket\n");
    }
    printf("Socket created\n");
     
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 10000 );
     
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        printf("bind failed. Error\n");
        return 1;
    }
    printf("bind done\n");

    listen(socket_desc , 3);

    c = sizeof(struct sockaddr_in);
	pthread_t thread_id;
	
    while( (client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        printf("Connection accepted\n");
        if( pthread_create( &thread_id , NULL ,  connection_handler , (void*) &client_sock) < 0)
        {
            printf("could not create thread\n");
        }
        printf("Handler assigned\n");

        //TODO timer
    }
     
    if (client_sock < 0)
    {
        printf("accept failed\n");
        return 1;
    }
     
    return 0;
}
 
/**
 * @brief Funkce je spustena ve vlastnim vlakne a obstarava jednoho klienta, zpracovava prijmute zpravy
 * 
 * @param socket_desc socket uzivatele
 * @return void* 
 */
void *connection_handler(void *socket_desc)
{
    int sock = *(int*)socket_desc;
    int read_size;
    char *message , client_message[CLIENT_MSG_SIZE];
 
    //prijimani zpravy
    while( (read_size = recv(sock , client_message , CLIENT_MSG_SIZE , 0)) > 0 )
    {
        //end of string marker
        client_message[read_size] = '\0';
        printf("server prijmul: %s\n", client_message);	
		
        int i = 0;
        char *p = strtok(client_message, ",");
        char *params[3];

        while (p != NULL)
        {
            params[i++] = p;
            p = strtok(NULL, ",");
        }

        if (strcmp(params[1], RECONNECT_TO_GAME) == 0){

        }
        else if (strcmp(params[1], CREATE_NEW_ROOM) == 0){
            int i;
            for(i = 0; i < NUMBER_OF_ROOMS; i++){
                if(games[i].id_r == -1){
                    games[i].id_r = i;
                    games[i].state = STATE_IN_LOBBY;
                    games[i].array_p[0] = players[atoi(params[0])];
                    games[i].number_players = 1;
                    games[i].availability[0] = 1;
                    break;
                }
            }
    
            char text_number[8];
            sprintf(text_number, "%d", i);
            printf("id mistnosti: %s\n", text_number);

            char *msg = malloc(strlen("4,") + strlen(text_number) + 1);
            memcpy(msg, "4,", strlen("4,"));
            memcpy(msg + strlen("4,"), text_number, strlen(text_number));
            memcpy(msg + strlen("4,") + strlen(text_number), ";1", strlen(";1") + 1);
            puts("Odesilam:");
            puts(msg);
            write(sock, msg, sizeof(msg));
        }
        else if (strcmp(params[1], START_GAME) == 0){
            int player_id = atoi(params[0]);
            int g;
            int game_id;
            puts("id hrace:");
            char text_number[8];
            sprintf(text_number, "%d", player_id);
            puts(text_number);

            for (g = 0; g < NUMBER_OF_ROOMS;g++){
                if(games[g].array_p[0].id_p == player_id){
                    game_id = g;
                    break;
                }
            }
            printf("Id hry: %d\n", game_id);

            question q = questions[games[game_id].q_ids[games[game_id].round]];

            char *msg = malloc(strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-")+ strlen(q.ans2) + strlen("-") + strlen(q.ans3) + strlen("-")+ strlen(q.ans4) + 1);
            memcpy(msg, "5,", strlen("5,"));
            memcpy(msg + strlen("5,"), q.question, strlen(q.question)); //otazka
            memcpy(msg + strlen("5,") + strlen(q.question), ";", strlen(";")); 
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";"), q.ans1, strlen(q.ans1)); //odpoved 1
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1), "-", strlen("-"));
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-"), q.ans2, strlen(q.ans2)); //odpoved 2
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-") + strlen(q.ans2), "-", strlen("-")); 
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-") + strlen(q.ans2) + strlen("-"), q.ans3, strlen(q.ans3)); // odpoved 3 
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-") + strlen(q.ans2) + strlen("-") + strlen(q.ans3), "-", strlen("-")); 
            memcpy(msg + strlen("5,") + strlen(q.question) + strlen(";") + strlen(q.ans1) + strlen("-") + strlen(q.ans2) + strlen("-") + strlen(q.ans3)+ strlen("-"), q.ans4, strlen(q.ans4) + 1); // odpoved 4
            puts("Odesilam:");
            puts(msg);

            int p;
            for (p = 0; p < 3; p++){
                if (games[game_id].availability[p] == 1){
                    write(games[game_id].array_p[p].socket, msg, strlen(msg));
                }       
            }


        }
        else if (strcmp(params[1], CONNECT_TO_GAME) == 0){
            int game_id = atoi(params[2]);
            if(games[game_id].id_r == -1){
                puts("Nepovedlo se");
                //TODO odeslat chybu kterou si klient prebere
                return;
            }
            else if(games[game_id].number_players == 3){
                puts("taky nevyšlo tů mač pípl");
                //TODO odeslat chybu kterou si klient prebere
                /*char *msg = malloc(strlen("2,") + "-1" + 1);
                memcpy(msg, "2,", strlen("2,"));
                memcpy(msg + strlen("2,"), "-1" , strlen("-1" )+1);
                puts("Odesilam:");
                puts(msg);*/
                return;
            }
            
            int i;
            //od jedný, když nula je admin a odpojí se, hra bájbáj
            for (i = 1; i < 3; i++){
                if (games[game_id].availability[i] == 0){
                    games[game_id].array_p[i] = players[atoi(params[0])];
                    games[game_id].number_players++;
                    games[game_id].availability[i] = 1;
                    break;
                }  
            } 

            char text_number[8];
            sprintf(text_number, "%d", games[game_id].number_players);
            printf("pocet hracu: %s\n", text_number);

            char *msg = malloc(strlen("2,") + strlen(text_number) + 1);
            memcpy(msg, "2,", strlen("2,"));
            memcpy(msg + strlen("2,"), text_number, strlen(text_number)+1);
            puts("Odesilam:");
            puts(msg);

            int p;
            for (p = 1; p < 3; p++){
                if (games[game_id].availability[p] == 1){
                    write(games[game_id].array_p[p].socket, msg, sizeof(msg));
                }       
            }

            char game_id_text[8];
            sprintf(game_id_text, "%d", game_id);

            char *msg_for_admin = malloc(strlen("4,") + strlen(game_id_text) + strlen(text_number) + 1);
            memcpy(msg_for_admin, "4,", strlen("4,"));
            memcpy(msg_for_admin + strlen("4,"), game_id_text, strlen(game_id_text));
            memcpy(msg_for_admin + strlen("4,") + strlen(game_id_text), ";", strlen(";"));
            memcpy(msg_for_admin + strlen("4,") + strlen(game_id_text) + strlen(";"), text_number, strlen(text_number)+1);
            puts("Odesilam:");
            puts(msg_for_admin);
            write(games[game_id].array_p[0].socket, msg_for_admin, sizeof(msg_for_admin));

        } 
        else if (strcmp(params[1], SEND_QUIZ_ANSWER) == 0){
            int player_id = atoi(params[0]);
            int answer = atoi(params[2]);
            int game_id;

            int g;
            for (g = 0; g < NUMBER_OF_ROOMS;g++){
                if(games[g].array_p[0].id_p = player_id){
                    game_id = g;
                    break;
                }
            }

            if (answer == questions[games[game_id].q_ids[games[game_id].round]].correct){
                players[player_id].points += 1;
            }

            char points[8];
            sprintf(points, "%d", players[player_id].points);
            char correct[8];
            sprintf(correct, "%d", questions[games[game_id].q_ids[games[game_id].round]].correct);

            char *msg = malloc(strlen("6,") + strlen(points) + strlen(";") + strlen(correct) + 1);
            memcpy(msg, "6,", strlen("6,"));
            memcpy(msg + strlen("6,"), points, strlen(points));
            memcpy(msg + strlen("6,") + strlen(points), ";", strlen(";"));
            memcpy(msg + strlen("6,") + strlen(points) + strlen(";"), correct, strlen(correct) + 1);
            puts("Odesilam:");
            puts(msg);
            
            write(sock, msg, sizeof(msg));
            
        }
        else if (strcmp(params[1], PAUSE_GAME) == 0){
            
        }
        else if (strcmp(params[1], LEAVE_GAME) == 0){
            
        }
        else if (strcmp(params[1], REQ_ID) == 0){
            int i;
            for(i = 1; i < NUMBER_OF_PLAYERS; i++){
                if(players[i].id_p == -1){
                    players[i].id_p = i;
                    players[i].socket = sock;
                    players[i].points = 0;
                    break;
                }
            }
            char text_number[8];
            sprintf(text_number, "%d", i);
            printf("id: %s\n", text_number);

            char *msg = malloc(strlen("1,") + strlen(text_number) + 1);
            memcpy(msg, "1,", strlen("1,"));
            memcpy(msg + strlen("1,"), text_number, strlen(text_number)+1);
            puts("Odesilam:");
            puts(msg);
            write(sock, msg, sizeof(msg));
        }
      
	    memset(client_message, 0, CLIENT_MSG_SIZE);
    }
     
    if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("recv failed");
    }
         
    return 0;
} 

/*
question* prepare_q(){
    question* questions = calloc(2,sizeof(question));

    questions[0].question = "Jakou barvu má sluníčko";
    questions[0].ans1 = "modrá";
    questions[0].ans2 = "žlutá";
    questions[0].ans3 = "černá";
    questions[0].ans4 = "růžová";
    questions[0].correct = 2;

    questions[1].question = "Kdo je nejlepší cvičící na UPS";
    questions[1].ans1 = "Skupa";
    questions[1].ans2 = "Pepa";
    questions[1].ans3 = "Adam";
    questions[1].ans4 = "Bořek";
    questions[1].correct = 1;

    return questions;
}*/