// CPSC/ECE 3220 resource allocation code
//
// you need to add synchronization variables and calls to lock, wait,
//   and signal, as well as the necessary init and destroy functions
//
// search for ADD in comments
//
// compile with "gcc -Wall resource.c -pthread"
// run with "./a.out" or "valgrind --tool=helgrind ./a.out"


#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>


#define THREADS 20
#define RESOURCES 4


// --------------------------------------
// -- resource object implemented in C --
// --------------------------------------

typedef struct resource_type_tag{

    // state variables

    int type;             // field to distinguish resource type
    int total_count;      // total number of resources of this type
    int available_count;  // number of currently available resources
    char *status;         // pointer to status vector on heap; encoding:
                          //     0 = available, 1 = in use
    char *owner;          // pointer to owner vector on heap; encoding:
                          //     0 to 127 are valid owner ids,
                          //     -1 is invalid owner id
    int signature;        // signature for run-time type checking; put
                          //     after a vector to catch some overflows


    // synchronization variables

	// you need to ADD them here
  pthread_mutex_t mutex;
  pthread_cond_t CV;


    // methods other than init (constructor) and reclaim (destructor)

    int (*allocate)( struct resource_type_tag *self, int tid );
    void (*release)( struct resource_type_tag *self, int tid, int rid );
    void (*print)( struct resource_type_tag *self );

} resource_t;


// helper functions

int resource_check( resource_t *r ){

    // does not need locking operations since this is a helper function and
    //   is called by the public methods and the destructor

    if( r->signature == 0x1E5041CE ) return 0;
    else return 1;
}

void resource_error( int code ){

    // does not need locking operations since this is a helper function and
    //   is called by the constructor, the public methods, and the destructor

    switch( code ){
        case 0:  printf( "**** malloc error for resource object\n" );
                 break;
        case 1:  printf( "**** malloc error for status vector\n" );
                 break;
        case 2:  printf( "**** malloc error for owner vector\n" );
                 break;
        case 3:  printf( "**** could not initialize lock for resource\n" );
                 break;
        case 4:  printf( "**** could not initialize condition for resource\n" );
                 break;
        case 5:  printf( "**** reclaim argument is not a valid resource\n" );
                 break;
        case 6:  printf( "**** print argument is not a valid resource\n" );
                 break;
        case 7:  printf( "**** allocate signature check failed\n" );
                 break;
	case 8:  printf( "**** search for resource failed\n" );
		 break;
	case 9:  printf( "**** release signature check failed\n" );
	         break;
	case 10: printf( "**** release rid bounds check failed\n" );
		 break;
	case 11: printf( "**** release ownership check failed\n" );
		 break;
        default: printf( "**** unknown error code\n" );
    }
    exit( 0 );
}


    // prototypes for forward referencing of public methods in init
    int resource_allocate( struct resource_type_tag *, int );
    void resource_release( struct resource_type_tag *, int, int );
    void resource_print( struct resource_type_tag * );


// init function serves the role of a constructor

resource_t * resource_init( int type, int total ){
    resource_t *r;
    int i, rc;

    // does not need locking operations since the lock is created
    //   in this function

    r = malloc( sizeof( resource_t ) );   // obtain memory for struct
    if( r == NULL ) resource_error( 0 );

    r->type = type;                       // set data fields
    r->total_count = total;
    r->available_count = total;

    r->status = malloc( total + 1 );      // obtain memory for vector
    if( r->status == NULL )               //     extra entry allows
        resource_error( 1 );              //     faster searching
    for( i = 0; i <= total; i++ )         // 0 = available, 1 = in use
        r->status[i] = 0;

    r->owner = malloc( total );           // obtain memory for vector
    if( r->owner == NULL )
        resource_error( 2 );
    for( i = 0; i < total; i++ )          // -1 = invalid owner id
        r->owner[i] = -1;

    r->signature = 0x1E5041CE;

    // ADD call to pthread_mutex_init() with rc as return code for
    //   each mutex
    rc = pthread_mutex_init( &r->mutex, NULL);
    if( rc != 0 ) resource_error( 3 );

    // ADD call to pthread_cond_init() with rc as return code for
    //   each condition variable
    rc = pthread_cond_init( &r->CV, NULL);
    if( rc != 0 ) resource_error( 4 );

    r->print = &resource_print;           // set method pointers
    r->allocate = &resource_allocate;
    r->release = &resource_release;

    return r;
}


// reclaim function serves the role of a destructor

void resource_reclaim( resource_t *r ){

    // does not need locking operations since the lock is destroyed
    //   in this function

    if( resource_check( r ) ) resource_error( 5 );

    // ADD call to pthread_cond_destroy() for each condition variable
    pthread_cond_destroy( &r->CV);

    // ADD call to pthread_mutex_destroy() for each mutex
    pthread_mutex_destroy( &r->mutex);

    free( r->owner );
    free( r->status );
    free( r );
}


// allocate, release, and print would be public methods in an object


int resource_allocate( struct resource_type_tag *self, int tid ){
    int rid;

    // you need to ADD synchronization operations to this function
    //   as appropriate; follow the patterns in the textbook

    pthread_mutex_lock(&self->mutex);
    while (self->available_count == 0) {
      pthread_cond_wait(&self->CV,&self->mutex);
    }

    if( resource_check( self ) )          // signature check
        resource_error( 7 );

    // assertion before proceeding: self->available_count != 0

    rid = 0;                              // initialize search index
    self->status[self->total_count] = 0;  // extra entry is always available
    while( self->status[rid] != 0)        // search until available entry found
        rid++;
    if( rid >= self->total_count)         // bounds check of result
        resource_error( 8 );

    self->status[rid] = 1;                // mark this entry as in use
    self->owner[rid] = tid;               // record which thread has it
    self->available_count--;              // decr count of available resources
    pthread_cond_broadcast(&self->CV);
    pthread_mutex_unlock(&self->mutex);
    return rid;
}

void resource_release( struct resource_type_tag *self, int tid, int rid ){

    // you need to ADD synchronization operations to this function
    //   as appropriate; follow the patterns in the textbook

    pthread_mutex_lock(&self->mutex);
    while (self->available_count == self->total_count) {
      pthread_cond_wait(&self->CV,&self->mutex);
    }

    if( resource_check( self ) )          // signature check
        resource_error( 9 );
    if( rid >= self->total_count)         // bounds check of argument
        resource_error( 10 );
    if( self->owner[rid] != tid)          // check ownership match
        resource_error( 11 );

    self->status[rid] = 0;                // mark this entry as available
    self->owner[rid] = -1;                // reset ownership
    self->available_count++;              // incr count of available resources
    pthread_cond_broadcast(&self->CV);
    pthread_mutex_unlock(&self->mutex);

}

void resource_print( struct resource_type_tag *self ){
    int i;

    // you need to ADD synchronization operations to this function
    //   as appropriate; follow the patterns in the textbook

    pthread_mutex_lock(&self->mutex);

    if( resource_check( self ) )          // signature check
        resource_error( 6 );

    printf( "-- resource table for type %d --\n", self->type );
    for(i = 0; i < self->total_count; i++){
        printf(" resource #%d: %d,%d\n", i, self->status[i], self->owner[i] );
    }
    printf("-------------------------------\n");

    pthread_mutex_unlock(&self->mutex);

}


// --------------------------------
// -- end of resource definition --
// --------------------------------



// argument vector for threads

typedef struct{
    resource_t *rp;
    int id;
} argvec_t;



// worker thread skeleton

void *worker( void *ap ){
    resource_t *resource = ((argvec_t *)ap)->rp;
    int thread_id = ((argvec_t *)ap)->id;
    int resource_id;

    resource_id = (resource->allocate)( resource, thread_id );

    printf( "thread #%d uses resource #%d\n", thread_id, resource_id );
    sleep(1);

    (resource->release)( resource, thread_id, resource_id );

    return NULL;
}


// observer thread

void *observer( void *ap ){
    resource_t *resource = ((argvec_t *)ap)->rp;
    int i;

    for( i = 0; i < 2; i++ ){
        sleep( 2 );
        (resource->print)( resource );
    }

    return NULL;
}


// --------------------------------------------
// -- test driver with one resource instance --
// --------------------------------------------

int main(int argc, char **argv){
    pthread_t threads[ THREADS + 1 ];
    argvec_t args[ THREADS + 1 ];
    int i;
    resource_t *resource_1;

    resource_1 = resource_init( 1, RESOURCES );

    (resource_1->print)( resource_1 );

    for( i = 0; i < THREADS; i++ ){
        args[i].rp = resource_1;
        args[i].id = i;
        if( pthread_create( &threads[i], NULL, &worker, (void *)(&args[i]) ) ){
            printf("**** could not create worker thread %d\n", i);
            exit( 0 );
        }
    }

    i = THREADS;
    args[i].rp = resource_1;
    args[i].id = i;
    if( pthread_create( &threads[i], NULL, &observer, (void *)(&args[i]) ) ){
        printf("**** could not create observer thread\n");
        exit( 0 );
    }

    for( i = 0; i < (THREADS+1); i++ ){
        if( pthread_join( threads[i], NULL ) ){
            printf( "**** could not join thread %d\n", i );
            exit( 0 );
        }
    }

    (resource_1->print)( resource_1 );

    resource_reclaim( resource_1 );

    return 0;
}
