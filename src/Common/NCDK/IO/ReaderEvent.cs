/* Copyright (C) 2002-2007  The Jmol Development Team
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT Any WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

 namespace NCDK.IO
{
    /// <summary>
    /// Signals that something has happened in a file reader. This class is
    /// primarily in place for future development when additional information
    /// may be passed to <see cref="Listener.IReaderListener"/>s.
    /// </summary>
    // @cdk.module io
    // @author Bradley A. Smith <bradley@baysmith.com>
    public class ReaderEvent
    {
        public object Source { get; protected set; }

        /// <summary>
        /// Creates a reader event.
        /// </summary>
        /// <param name="source">the object on which the event initially occurred.</param>
        public ReaderEvent(object source)
        {
            Source = source;
        }
    }
}
