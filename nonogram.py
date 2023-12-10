import tkinter;

from tkinter import *
from tkinter import ttk;
from tkinter.filedialog import askopenfilename;

GRID_SIZE = 30          # rozmiar kratki nonogramu
BORDERS = 20            # minimalna granica/margines od krawędzi okna
TOP_BORDER = 80         # branica/margines z góry dla górnej części canvasa
FRAME_MIN_WIDTH = 300   # minimalna szerokość okienka

class Application :
    def __init__( self, root ) :
        self.root = root
        self.root.title( 'Nonogram' )

        self.frame = ttk.Frame(
            self.root,
            width = FRAME_MIN_WIDTH,
            height = TOP_BORDER
        )
        self.frame.pack()

        self.pathLabelText = StringVar()
        self.pathLabelText.set( 'Nie wybrano z nonogramem!' )

        self.mouseX = 100                                                       # współrzędna X kursora myszy
        self.mouseY = 0                                                         # współrzędna Y kursora myszy
        self.mousePressed = 0                                                   # flaga czy klawisz myszy został kliknięty
        self.mouseOver = 0                                                      # flaga czy kursor myszy znajduje się nad widgetem

        self.solve = FALSE                                                      # flaga czy rozwiązano nonogram
        
        self.init_widgets()
    
    def init_widgets( self ) :                                                  # INICJACJA WIDGETÓW
        self.pathLabel = ttk.Label(                                             # etykieta
            self.root,
            textvariable = self.pathLabelText
        ).place(
            x = BORDERS,
            y = BORDERS / 2
        )

        ttk.Button(                                                             # przycisk do wybrania pliku z nonogramem
            self.root,
            command = self.get_nonogram_file,
            text = 'Wybierz plik z nonogramem'
        ).place(
            x = BORDERS,
            y = BORDERS * 2
        )

        self.clear = ttk.Button(                                                # przycisk do czyszczenia nonogramemu
            self.root,
            command = self.clear_nonogram,
            text = 'Wyczyść'
        )

        self.canvas = tkinter.Canvas(                                           # canvas na którym będzie rysowany nonogram
            master = self.root,
            width = 0,
            height = 0,
            bg = 'white'
        )

        self.canvas.place(
            x = BORDERS,
            y = TOP_BORDER
        )

        self.canvas.bind( '<Motion>', self.mouseMotion )                        # dodanie zdarzenia poruszania myszą dla canvasa
        self.canvas.bind( '<Button-1>', self.mousePress )                       # dodanie zdarzenia kliknięcia klawisza myszy dla canvasa
        self.canvas.bind( '<ButtonRelease-1>', self.mouseRelease )              # dodanie zdarzenia zwolnienia klawisza myszy dla canvasa
        self.canvas.bind( '<Enter>', self.mouseEnter )                          # dodanie zdarzenia zwolnienia klawisza myszy dla canvasa
        self.canvas.bind( '<Leave>', self.mouseLeave )                          # dodanie zdarzenia zwolnienia klawisza myszy dla canvasa

        ##self.canvas.pack

    def get_nonogram_file( self ) :                                             # ODCZYTANIE PLIKU Z NONOGRAMEM
        filePath = askopenfilename( filetypes = [ ( "Nonogram" , "*.nono" ) ] ) # plik z nonogramem powinien mieć rozszerzenie *.nono
        fileName = str.split( filePath, '/' )[ -1 ]
        self.root.title( 'Nonogram :: %s' % fileName )
        self.pathLabelText.set( 'Wybrany plik z nonogramem: %s' % fileName )
        self.file = open( filePath, 'r', encoding = 'utf-8' )

        self.mousePressed = FALSE
        self.mouseOver = FALSE
        self.solve = FALSE

        self.calculate_params()
        self.update_frame_and_canvas()
        self.draw()

    def clear_nonogram( self ) :                                                # WYZEROWANIE TABLICY Z NONOGRAMEM
        if self.solve == FALSE :
            self.nonogram = [ [ 0 for i in range( self.grids[ 0 ] ) ] for j in range( self.grids[ 1 ] ) ]
            self.draw()

    def calculate_params( self ) :                                              # OBLICZANIE WSZYSKICH WARTOŚCI LICZBOWYCH NA PODSTAWIE WYBRANEGO PLIKU Z NONOGRAMEM

        grids = str.split( self.file.readline() )

        self.grids = [ int( grids[ 0 ] ), int( grids[ 1 ] ) ]                   # wymiary X oraz Y obrazka nonogramu
        self.rows = []                                                          # liczby w wierszach
        self.cols = []                                                          # liczby w kolumnach
        self.nonogram = [ [ 0 for i in range( self.grids[ 0 ] ) ] for j in range( self.grids[ 1 ] ) ]   # tablica na nonogram o wymiarach X na Y wypełniona zerami ( X i Y pobrany z self.grids )
        self.maxNumberRows = 0                                                  # najdwiększa ilość numerów w wierszu z numerami pionowymi, wyświetlonymi po prawej stornie nonogramu
        self.maxNumberCols = 0                                                  # największa ilość numerów w kolumnie z numerami poziomymi, wyświetlonymi na górze nonogramu

        for i in range( 0, self.grids[ 0 ] ) :                                  # wczytanie liczb dla wszystkich kolumn
            self.cols.append( [ int( a ) for a in self.file.readline().split() ] )

        for i in range( 0, self.grids[ 1 ] ) :                                  # wczytanie liczb dla wszystkich wierszów
            self.rows.append( [ int( a ) for a in self.file.readline().split() ] )

        for col in self.cols :                                                  # pobieranie największej ilości numerów w kolumnie
            length = len( col )
            if self.maxNumberCols < length : self.maxNumberCols = length

        for row in self.rows :                                                  # pobieranie największej ilości numerów w wierszu
            length = len( row )
            if self.maxNumberRows < length : self.maxNumberRows = length

    def update_frame_and_canvas( self ) :                                       # AKTUALIZACJA WYMIARÓW OKIENKA ORAZ CANVASA

        canvasWidth = ( self.maxNumberRows + self.grids[ 0 ] ) * GRID_SIZE      # obliczenie nowej szerokości canvasa
        canvasHeight = ( self.maxNumberCols + self.grids[ 1 ] ) * GRID_SIZE     # obliczneie nowej wysokości canvasa

        self.frame.config(                                                      # podstawnienie nowych wymiarów okienka po wczytaniu nonogramu
            width = ( canvasWidth + 2 * BORDERS > FRAME_MIN_WIDTH and canvasWidth + 2 * BORDERS or FRAME_MIN_WIDTH ),
            height = BORDERS + TOP_BORDER + canvasHeight
        )

        self.frame.update()                                                     # aktualizacja okienka

        self.canvas.config(                                                     # podstawienie nowych wymiarów canvasa po wczytaniu nonogramu
            width = canvasWidth,
            height = canvasHeight
        )
        
        self.canvas.place(                                                      # wyśrodkowanie canvasa wewnątrz okienka
            x = ( self.frame.winfo_reqwidth() - canvasWidth ) / 2
        )

        self.clear.place(
            x = self.frame.winfo_reqwidth() - self.clear.winfo_reqwidth() - BORDERS,
            y = BORDERS * 2
        )

        self.canvas.update()                                                    # aktualizacja canvasa


    def draw( self ) :                                                          # NARYSOWANIE NA CANVASIE

        self.canvas.delete( 'all' )                                             # wyczyszczenie canvasa

        color = '#f5f5f5'                                                       # podświetlenie kolumny i wiersza wskazanego myszą
        gridX = int( self.mouseX / GRID_SIZE )
        gridY = int( self.mouseY / GRID_SIZE )
        if gridX >= self.maxNumberRows and gridY >= self.maxNumberCols and self.solve == FALSE :        # podświetlenie tylko wtedy kiedy kursor znajduje się nad nonogramem
            self.canvas.create_line(
                ( gridX + .5 ) * GRID_SIZE,
                0,
                ( gridX + .5 ) * GRID_SIZE,
                self.canvas.winfo_height(),
                width = GRID_SIZE,
                fill = color
            )
            self.canvas.create_line(
                0,
                ( gridY + .5 ) * GRID_SIZE,
                self.canvas.winfo_width(),
                ( gridY + .5 ) * GRID_SIZE,
                width = GRID_SIZE,
                fill = color
            )
        
        color = '#333'
        for y in range( 0, len( self.nonogram ) ) :                             # rysowanie nonogramu
            for x in range( 0, len( self.nonogram[ y ] ) ) :
                if self.nonogram[ y ][ x ] == 1 :
                    self.canvas.create_rectangle(
                        ( self.maxNumberRows + x ) * GRID_SIZE + 2,
                        ( self.maxNumberCols + y ) * GRID_SIZE + 2,
                        ( self.maxNumberRows + x + 1 ) * GRID_SIZE - 1,
                        ( self.maxNumberCols + y + 1) * GRID_SIZE - 1,
                        fill = color,
                        outline = ''
                    )

        for i in range( 1, self.grids[ 0 ] ) :                                  # narysowanie pionowej siatki
            self.canvas.create_line(
                ( self.maxNumberRows + i ) * GRID_SIZE,
                0,
                ( self.maxNumberRows + i ) * GRID_SIZE,
                self.canvas.winfo_height(),
                fill = ( i % 5 == 0 and '#ddd' or '#eee' )                      # co piąta linia siatki jest ciemniejsza
            )

        for i in range( 1, self.grids[ 1 ] ) :                                  # narysowanie poziomej siatki
            self.canvas.create_line(
                0,
                ( self.maxNumberCols + i ) * GRID_SIZE,
                self.canvas.winfo_width(),
                ( self.maxNumberCols + i ) * GRID_SIZE,
                fill = ( i % 5 == 0 and '#ddd' or '#eee' )                      # co piąta linia siatki jest ciemniejsza
            )
        
                                                                                # linie oddzielająca liczby od nonogramu
        color = '#ccc'
        self.canvas.create_line(
            0,
            self.maxNumberCols * GRID_SIZE,
            self.canvas.winfo_width(),
            self.maxNumberCols * GRID_SIZE,
            fill = color
        )
        self.canvas.create_line(
            self.maxNumberRows * GRID_SIZE,
            0,
            self.maxNumberRows * GRID_SIZE,
            self.canvas.winfo_height(),
            fill = color
        )

        color = '#666'
        font = 'monospace 14 bold'
                                                                                # wypisanie liczb nad nonogramem
        for i in range( 0, self.grids[ 0 ] ) :
            for j in range( 0, len( self.cols[ i ] ) ) :
                self.canvas.create_text(
                    ( self.maxNumberRows + i ) * GRID_SIZE + GRID_SIZE / 2,
                    ( self.maxNumberCols - j ) * GRID_SIZE - GRID_SIZE / 2,
                    text = self.cols[ i ][ len( self.cols[ i ] ) - j - 1 ],
                    fill = color,
                    font = font
                )

                                                                                # wypisanie liczb po lewej stornie nonogramu
        for i in range( 0, self.grids[ 1 ] ) :
            for j in range( 0, len( self.rows[ i ] ) ) :
                self.canvas.create_text(
                    ( self.maxNumberRows - j ) * GRID_SIZE - GRID_SIZE / 2,
                    ( self.maxNumberCols + i ) * GRID_SIZE + GRID_SIZE / 2,
                    text = self.rows[ i ][ len( self.rows[ i ] ) - j - 1 ],
                    fill = color,
                    font = font
                )
        
        if self.solve == TRUE :                                                 # jeżeli rozwiązano pokaż komunikat
            self.canvas.create_rectangle(
                self.canvas.winfo_width() / 2 - 80,
                self.canvas.winfo_height() / 2 - 20,
                self.canvas.winfo_width() / 2 + 80,
                self.canvas.winfo_height() / 2 + 20,
                fill = '#fff',
                outline = ''
            )
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text = 'ROZWIAZANO!',
                fill = '#333',
                font = 'arial 16 bold'
            )

        self.canvas.update()                                                    # aktualizacja canvasa
    
    def is_resolved( self ) :                                                   # SPRAWDZENIE CZY NONOGRAM ZOSTAŁ ROZWIĄZANY
        if self.check_cols() and self.check_rows() :
            self.solve = TRUE
    
    def check_cols( self ) :                                                    # SPRAWDZENIE CZY WSZYSKIE KOLUMNY ZOSTAŁY POPRAWNIE ROZWIĄZANE
        for x in range( 0, len( self.nonogram[ 0 ] ) ) :
            numbers = []                                                        # tablica na długości grup zaznaczonych pół w danej kolumnie
            length = 0                                                          # długość grupy zaznaczonych pół w danej kolumnie
            for y in range( 0, len( self.nonogram ) ) :
                if self.nonogram[ y ][ x ] == 0 :
                    if length != 0 :
                        numbers.append( length )
                        length = 0
                else :
                    length = length + 1
            if length != 0 :
                numbers.append( length )
            if len( numbers ) == 0 :                                            # jeżeli w kolumnie nie ma żadnych zaznaczonych pól wpisuje ZERO dla tej kolumny
                numbers.append( 0 )
            if len( numbers ) == len( self.cols[ x ] ) :
                for i in range( 0, len( numbers ) ) :                           # porównanie wyliczonych powyżej wartości dla komunmy do tych poprawnych pobranych z odczytanego pliku
                    if numbers[ i ] != self.cols[ x ][ i ] :
                        return FALSE                                            # jeżeli którakolwiek z komumn będzie błędna zakańczamy sprawdzanie i zwracamy FAŁSZ jako wiadomość że któraś z kolumna jest błędnie rozwiązana
            else :
                return FALSE
        return TRUE                                                             # wracam TRAWDĘ jako wiadomość o tym że wszystki kolumny są poprawnie rozwiązane

    def check_rows( self ) :                                                    # SPRAWDZENIE CZY WSZYSTKIE WIERSZE ZOSTAŁY POPRAWNIE ROZWIĄZANE
        for y in range( 0, len( self.nonogram ) ) :
            numbers = []                                                        # tablica na długości grup zaznaczonych pół w danym wierszu
            length = 0                                                          # długość grupy zaznaczonych pół w danym wierszu
            for x in range( 0, len( self.nonogram[ 0 ] ) ) :
                if self.nonogram[ y ][ x ] == 0 :
                    if length != 0 :
                        numbers.append( length )
                        length = 0
                else :
                    length = length + 1
            if length != 0 :
                numbers.append( length )
            if len( numbers ) == 0 :                                            # jeżeli w wierszu nie ma żadnych zaznaczonych pól wpisuje ZERO dla tego wiersza
                numbers.append( 0 )
            if len( numbers ) == len( self.rows[ y ] ) :
                for i in range( 0, len( numbers ) ) :                           # porównanie wyliczonych powyżej wartości dla wierszy do tych poprawnych pobranych z odczytanego pliku
                    if numbers[ i ] != self.rows[ y ][ i ] :
                        return FALSE                                            # jeżeli którykolwiek z wierszy będzie błędny zakańczamy sprawdzanie i zwracamy FAŁSZ jako wiadomość że któryś z wierszy jest błędnie rozwiązana
            else :
                return FALSE
        return TRUE

    def mouseMotion( self, event ):                                             # ZDARZENIE PORUSZANIA KURSOREM MYSZY
        self.mouseX = event.x
        self.mouseY = event.y
        if self.mouseOver == TRUE :                                             # jeżeli kursor znajduje się nad widgetem odświerza rysunek w canvasie
            self.draw()

    def mousePress( self, event ):                                              # ZDARZENIE WCIŚNIĘCIA KLAWISZA MYSZY
        self.mousePressed = TRUE
        if self.mouseOver == TRUE and self.solve == FALSE :                     # jeżeli kursor znajduje się nad widgetem i nonogram nie jest rozwiązany zaznacza kliknięte pole i odświerza rysunek w canvasie
            gridX = int( self.mouseX / GRID_SIZE )
            gridY = int( self.mouseY / GRID_SIZE )
            if gridX >= self.maxNumberRows and gridY >= self.maxNumberCols :
                gridX -= self.maxNumberRows
                gridY -= self.maxNumberCols
                self.nonogram[ gridY ][ gridX ] = ( self.nonogram[ gridY ][ gridX ] == 0 and 1 or 0 )
            self.draw()
            self.is_resolved()

    def mouseRelease( self, event ):                                            # ZDARZENIE ZWOLNIENIA KLAWISZA MYSZY
        self.mousePressed = FALSE

    def mouseEnter( self, event ):                                              # ZDARZENIE NAJECHANIA KURSOREM MYSZY NA WIDGET
        self.mouseOver = TRUE

    def mouseLeave( self, event ):                                              # ZDARZENIE OPUSZCZENIA WIDGETA PRZEZ KURSOR MYSZY
        self.mouseOver = FALSE

if __name__ == '__main__' :
    root = tkinter.Tk()
    Application( root )
    root.mainloop()